import json
import os
import tarfile
import tempfile
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from itertools import groupby, islice
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Generic,
    Iterable,
    Iterator,
    List,
    TypeVar,
    Union,
)

import attrs
from sqlalchemy import Float, Integer, String
from tqdm import tqdm

from dql.node import DirType, get_path

if TYPE_CHECKING:
    from dql.listing import Listing


PROCESSING_BATCH_SIZE = 1000  # Batch size for inserting entries.

INSERT_ITEMS = "insert"  # Indexing format adds new objects.
UPDATE_ITEMS = "update"  # Indexing format extends objects with new properties.

T = TypeVar("T")


class IndexingFormat(ABC, Generic[T]):
    """
    Indexing formats allow additional transformations on indexed
    objects, such as listing contents of archives.
    """

    # Default processor action - add new items to the index or update them,
    # e.g. by adding new signals.
    action_type: str = INSERT_ITEMS

    @abstractmethod
    def filter(self, listing: "Listing", paths: List[str]) -> Iterator[T]:
        """Create a list of entries to process"""

    @abstractmethod
    def process(self, listing, entries):
        """Process an entry and return additional entries to store."""


@attrs.define
class ArchiveInfo:
    parent: str
    name: str
    id: int
    is_latest: bool
    partial_id: int

    @property
    def path(self):
        return get_path(self.parent, self.name)


ARCHIVE_INFO_FIELDS = [attr.name for attr in attrs.fields(ArchiveInfo)]


class TarFiles(IndexingFormat[ArchiveInfo]):
    """
    TarFiles indexes buckets containing uncompressed tar archives. The contents of
    the archives is indexed as well.
    """

    item_type = INSERT_ITEMS

    def filter(self, listing: "Listing", paths: List[str]) -> Iterator[ArchiveInfo]:
        for path in paths:
            for node in listing.expand_path(path):
                found = listing.find(
                    node,
                    ARCHIVE_INFO_FIELDS,
                    names=["*.tar"],
                )
                for row in found:
                    yield ArchiveInfo(*row)

    def process(self, listing: "Listing", entries):
        for entry in entries:
            yield from self.process_entry(listing, entry)

    def process_entry(
        self, listing: "Listing", parent: ArchiveInfo
    ) -> Iterator[Dict[str, Any]]:
        local_path = tempfile.gettempdir() + f"/dql_cache_{parent.id}"
        client = listing.client
        # Download tarball to local storage first.
        client.fs.get_file(client.get_full_path(parent.path), local_path)
        with tarfile.open(name=local_path, mode="r:") as tar:
            for info in tar:
                if info.isdir():
                    yield self.tardir_from_info(info, parent)
                elif info.isfile():
                    yield self.tarmember_from_info(info, parent)
        os.remove(local_path)
        listing.data_storage.update_type(parent.id, DirType.TAR_ARCHIVE)

    def tarmember_from_info(self, info, parent: ArchiveInfo) -> Dict[str, Any]:
        location = json.dumps(
            [
                {
                    "offset": info.offset_data,
                    "size": info.size,
                    "type": "tar",
                    "parent": parent.path,
                },
            ]
        )
        full_path = f"{parent.path}/{info.name}"
        parent_dir, name = full_path.rsplit("/", 1)
        return {
            "vtype": "tar",
            "dir_type": DirType.FILE,
            "parent_id": parent.id,
            "parent": parent_dir,
            "name": name,
            "checksum": "",
            "etag": "",
            "version": "",
            "is_latest": parent.is_latest,
            "last_modified": datetime.fromtimestamp(info.mtime, timezone.utc),
            "size": info.size,
            "owner_name": info.uname,
            "owner_id": str(info.uid),
            "location": location,
            "partial_id": parent.partial_id,
        }

    def tardir_from_info(self, info, parent: ArchiveInfo) -> Dict[str, Any]:
        full_path = f"{parent.path}/{info.name}".rstrip("/")
        parent_dir, name = full_path.rsplit("/", 1)
        return {
            "vtype": "tar",
            "dir_type": DirType.DIR,
            "parent_id": parent.id,
            "parent": parent_dir,
            "name": name,
            "checksum": "",
            "etag": "",
            "version": "",
            "is_latest": parent.is_latest,
            "last_modified": datetime.fromtimestamp(info.mtime, timezone.utc),
            "size": info.size,
            "owner_name": info.uname,
            "owner_id": str(info.uid),
            "partial_id": parent.partial_id,
        }


@attrs.define
class ObjectInfo:
    parent: str
    name: str
    id: int
    vtype: str
    location: str

    @property
    def path(self):
        return get_path(self.parent, self.name)


OBJECT_INFO_FIELDS = [attr.name for attr in attrs.fields(ObjectInfo)]


class LaionJSONPair(IndexingFormat[ObjectInfo]):
    """
    Load signals from .json files and attach them to objects with the same base name.
    """

    action_type = UPDATE_ITEMS

    IGNORED_EXTS = [".json", ".txt"]  # File extensions not to attach loaded signals to.

    def filter(self, listing: "Listing", paths: List[str]) -> Iterator[ObjectInfo]:
        for path in paths:
            for node in listing.expand_path(path):
                found = listing.find(
                    node,
                    OBJECT_INFO_FIELDS,
                    order_by=["parent", "name"],
                )
                for row in found:
                    yield ObjectInfo(*row)

    def process(self, listing: "Listing", entries):
        self._create_columns(listing)
        for _, group in groupby(entries, self._group):
            yield from self._process_group(listing, group)

    def _process_group(self, listing: "Listing", group: Iterable[ObjectInfo]) -> Any:
        # Create a map of extension to object info.
        nodes = {os.path.splitext(obj.name)[1]: obj for obj in group}
        json_obj = nodes.get(".json")
        if not json_obj:
            # No .json file in group. Ignore.
            return
        with listing.client.open_object(
            json_obj.path, json_obj.vtype, json_obj.location
        ) as f:
            data = json.load(f)
            if not isinstance(data, dict):
                # .json file contains something other than a json object. Ignore.
                return
            update = {
                col[0]: data.get(col[0]) for col in laionJSONColumns if data.get(col[0])
            }

        for ext, node in nodes.items():
            if ext in self.IGNORED_EXTS:
                continue
            yield (node.id, update)

    def _group(self, entry):
        """
        Group entries by paths sans the extension.
        This way 'path/000.jpg' and 'path/000.json' will be grouped
        together.
        """
        return os.path.splitext(entry.path)[0]

    def _create_columns(self, listing: "Listing"):
        for col_name, col_type in laionJSONColumns:
            listing.data_storage.add_bucket_signal_column(
                listing.client.uri, col_name, col_type
            )


# Signal columns for storing laion json data.
laionJSONColumns = (
    ("punsafe", Float()),
    ("pwatermark", Float()),
    ("similarity", Float()),
    ("hash", Integer()),
    ("caption", String()),
    ("url", String()),
    ("key", String()),
    ("status", String()),
    ("error_message", String()),
    ("width", Integer()),
    ("height", Integer()),
    ("original_width", Integer()),
    ("original_height", Integer()),
    ("md5", String()),
)


async def apply_processors(
    listing: "Listing", path: str, processors: List[IndexingFormat]
):
    async def insert_items(items):
        await listing.data_storage.insert_entries(items)

    async def update_items(items):
        for item in items:
            (node_id, values) = item
            listing.data_storage.update_node(node_id, values)

    for processor in processors:
        if processor.action_type == INSERT_ITEMS:
            func = insert_items
        elif processor.action_type == UPDATE_ITEMS:
            func = update_items

        listing = listing.clone()
        with tqdm(desc="Processing", unit=" objects") as pbar:
            entries = processor.filter(listing, [path])
            results = processor.process(listing, entries)
            for batch in _batch(results, PROCESSING_BATCH_SIZE):
                pbar.update(len(batch))
                await func(batch)
        if processor.action_type == INSERT_ITEMS:
            listing.data_storage.inserts_done()


def _batch(it, size):
    while batch := list(islice(it, size)):
        yield batch


indexer_formats: Dict[str, Union[List[IndexingFormat], IndexingFormat]] = {
    "tar-files": TarFiles(),
    "json-pair": LaionJSONPair(),
    "webdataset": [TarFiles(), LaionJSONPair()],
}

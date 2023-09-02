from __future__ import annotations

from abc import ABC, abstractmethod
from functools import cached_property
from typing import TYPE_CHECKING, Any, ClassVar

import attrs
import pymongo.database
from pymongo import IndexModel

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

    from pymongo.collection import Collection


@attrs.define
class Index:
    """Represent a Mongo index

    :var keys: Document fields to add to an index. Mirrors `keys` from :class:`pymongo.collection.IndexModel`
    :var unique: Unique constraint, boolean
    """

    keys: str | Sequence[tuple[str, int | str | Mapping[str, Any]]]
    unique: bool = False

    def to_dict(self) -> dict[str, Any]:
        return attrs.asdict(self)


class MongoRepositoryMixin(ABC):
    """A mixin class that provides with a proxy to a defined Mongo collection.

    It also takes care of indexes, which can be defined as a class attribute.

    :cvar collection_name: A name of a collection to connect to
    :cvar indexes: A list of indexes to create for the collection.
                    It syncs indexes every first access to the collection,
                    meaning that all the old indexes will be deleted and new added.
    """

    collection_name: ClassVar[str]
    indexes: ClassVar[list[Index] | None] = None

    @abstractmethod
    def get_database(self) -> pymongo.database.Database:
        """Return a database instance."""

    @cached_property
    def _database(self) -> pymongo.database.Database:
        return self.get_database()

    @cached_property
    def _collection(self) -> Collection:
        collection: Collection = self._database[self.collection_name]
        default_indexes = ['_id_']
        skip_indexes: list[Index] = []
        indexes_to_remove: set[str] = set()

        if not self.indexes:
            return collection

        for name, index_data in collection.index_information().items():
            if name in default_indexes:
                continue

            index = Index(keys=index_data['key'], unique=index_data.get('unique', False))

            if index in self.indexes:
                skip_indexes.append(index)
            else:
                indexes_to_remove.add(name)

        for name in indexes_to_remove:
            collection.drop_index(name)

        indexes_to_create = [
            IndexModel(index.keys, unique=index.unique)
            for index in filter(lambda index: index not in skip_indexes, self.indexes)
        ]
        if indexes_to_create:
            collection.create_indexes(indexes_to_create)

        return collection

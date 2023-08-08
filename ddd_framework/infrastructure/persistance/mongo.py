from abc import ABC
from functools import cached_property
from typing import Any, Mapping, Optional, Sequence, Union

import attrs
from pymongo import IndexModel, MongoClient
from pymongo.collection import Collection


@attrs.define
class Index:
    keys: Union[str, Sequence[tuple[str, Union[int, str, Mapping[str, Any]]]]]
    unique: bool = False

    def to_dict(self) -> dict:
        return attrs.asdict(self)


class MongoRepository(ABC):
    collection_name: str = None
    indexes: Optional[list[Index]] = None

    def __init__(self, db_name: str, **kwargs):
        self._database = MongoClient(**kwargs)[db_name]

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

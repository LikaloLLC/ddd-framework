from __future__ import annotations

import warnings
from abc import ABC
from datetime import datetime
from typing import Any, Protocol, TypeVar

import cattrs
from attr import define, field, make_class

from ddd_framework.utils.types import get_generic_type


# region "Event"
@define(kw_only=True)
class Event:
    """A Domain event"""

    time: datetime = field(factory=datetime.now)


# endregion


# region "Value Object"
@define(kw_only=True)
class ValueObject:
    """A Value Object"""


# endregion


# region "Identity"
@define(kw_only=False, frozen=True)
class Id(ValueObject):
    """An identifier"""

    id: str | int

    @classmethod
    def from_raw_id(cls, raw_id: str | int) -> Id:
        return cls(id=raw_id)


def NewId(name: str, base: type[Id] = Id) -> type[Id]:
    """Create a new identifier's type."""
    warnings.warn('Id class will be removed in the next update', DeprecationWarning, stacklevel=2)

    return make_class(name, attrs={}, bases=(base,))


def structure_id(value: Any, _klass: type[Id]) -> Id:
    if isinstance(value, dict):
        return _klass(**value)
    return _klass(id=value)


cattrs.register_structure_hook(Id, structure_id)

EntityId = Any


# endregion


# region "Entity"
@define(kw_only=True, eq=False)
class Entity:
    """Represent an entity."""

    id: EntityId | Id | None = field(default=None)

    def __hash__(self) -> int:
        # TODO: Fix "Item "None" of "Id | None" has no attribute "id""
        return hash(self.id.id) if isinstance(self.id, Id) else hash(self.id)


# endregion


# region "Aggregate"
@define(kw_only=True, eq=True)
class Aggregate(ABC, Entity):
    """Represent an aggregate."""


# endregion


# region "Repository"
AggregateType_co = TypeVar('AggregateType_co', bound=Aggregate, covariant=True)


class IRepository(Protocol[AggregateType_co]):
    """A domain interface of an aggregate's repository."""

    @property
    def aggregate_cls(self) -> AggregateType_co:
        return get_generic_type(self.__class__)  # type: ignore


# endregion

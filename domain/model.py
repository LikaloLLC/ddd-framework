from abc import ABC
from datetime import datetime
from typing import Any, Optional, Protocol, Type, TypeVar, Union

from attr import define, field, make_class
import cattrs

from ddd_framework.utils.types import get_generic_type


# region "Event"
@define(kw_only=True)
class Event:
    """A Domain event"""

    time: datetime = field(factory=datetime.now)


# region "Value Object"
@define(kw_only=True)
class ValueObject:
    """A Value Object"""


# endregion

# region "Identity"
@define(kw_only=False, frozen=True)
class Id(ValueObject):
    """An identifier"""

    id: Union[str, int]

    @classmethod
    def from_raw_id(cls, raw_id: Union[str, int]) -> 'Id':
        return cls(id=raw_id)


def NewId(name: str, base: Id = Id):
    """Create a new identifier's type."""
    return make_class(name, attrs={}, bases=(base,))


def structure_id(value: Any, _klass: Type) -> Id:
    if isinstance(value, dict):
        return _klass(**value)
    return _klass(id=value)

cattrs.register_structure_hook(Id, structure_id)


# endregion


# region "Entity"
@define(kw_only=True, eq=False)
class Entity:
    """Represent an entity."""

    id: Optional[Id] = field(default=None)

    def __hash__(self):
        return hash(self.id.id)


# endregion


# region "Aggregate"
@define(kw_only=True, eq=True)
class Aggregate(ABC, Entity):
    """Represent an aggregate."""


# endregion


# region "Repository"
AggregateType = TypeVar('AggregateType', bound=Aggregate, covariant=True)


class IRepository(Protocol[AggregateType]):
    """A domain interface of an aggregate's repository."""

    @property
    def aggregate_cls(self) -> AggregateType:
        return get_generic_type(self.__class__)


# endregion

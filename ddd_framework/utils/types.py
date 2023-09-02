from __future__ import annotations

from typing import Any, get_args


def get_generic_type(cls: type[Any]) -> Any:
    return get_args(cls.__orig_bases__[0])[0]

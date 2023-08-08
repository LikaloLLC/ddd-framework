from typing import get_args


def get_generic_type(cls: type) -> type:
    return get_args(cls.__orig_bases__[0])[0]

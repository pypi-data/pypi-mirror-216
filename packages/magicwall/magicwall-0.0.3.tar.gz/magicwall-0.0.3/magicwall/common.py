#!/usr/bin/env python3

"""Common stuff shared among modules"""

from collections.abc import Mapping, MutableMapping, Sequence
from typing import TypeAlias, Union

GenMapVal: TypeAlias = Union[None, bool, str, float, int, "GenMapArray", "GenMap"]
GenMapArray: TypeAlias = Sequence[GenMapVal]
GenMap: TypeAlias = Mapping[str, GenMapVal]
MutableGenMap: TypeAlias = MutableMapping[str, GenMapVal]


class Tag:
    """An EXIF tag stub"""

    values: str

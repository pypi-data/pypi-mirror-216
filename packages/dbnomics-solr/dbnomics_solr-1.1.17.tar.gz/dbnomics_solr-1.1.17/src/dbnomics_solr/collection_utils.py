from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from collections.abc import Mapping

K = TypeVar("K")
V = TypeVar("V")


def without_none_values(d: Mapping[K, V]) -> Mapping[K, V]:
    """Return a copy of d without None values."""
    return {k: v for k, v in d.items() if v is not None}

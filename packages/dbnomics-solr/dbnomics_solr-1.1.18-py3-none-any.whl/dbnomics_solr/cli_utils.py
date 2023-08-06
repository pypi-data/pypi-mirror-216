from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterator

__all__ = ["list_callback"]


def list_callback(values: list[str]) -> list[str]:
    """Parse comma-separated values."""

    def iter_values() -> Iterator[str]:
        for value in values:
            for part in value.split(","):
                yield part.strip()

    return list(iter_values())

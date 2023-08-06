from __future__ import annotations

__all__ = ["english_join"]


def english_join(items: list[str]) -> str:
    """Return a string enumerating the items separated by a comma, except for the last one using the "and" separator."""
    return ", ".join(items[:-2] + [" and ".join(items[-2:])])

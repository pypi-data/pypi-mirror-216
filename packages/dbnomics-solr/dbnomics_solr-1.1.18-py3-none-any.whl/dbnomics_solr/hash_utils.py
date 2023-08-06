from __future__ import annotations

from typing import TYPE_CHECKING, cast

from dirhash import dirhash

if TYPE_CHECKING:
    from pathlib import Path


def compute_dir_hash(dir_path: Path, /, *, jobs: int = 1) -> str:
    """Compute a hash for a directory in an opinionated way.

    Follows the [dirhash standard](https://github.com/andhus/dirhash).
    """
    return cast(str, dirhash(dir_path, algorithm="sha1", jobs=jobs))

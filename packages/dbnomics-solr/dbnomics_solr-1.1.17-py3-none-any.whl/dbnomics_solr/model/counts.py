from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

__all__ = ["Counts"]


class Counts(BaseModel):
    dataset_count: int
    id: Literal["_counts"] = "_counts"
    provider_count: int
    series_count: int

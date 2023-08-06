"""Domain-level service to delete data related to a dataset."""

from __future__ import annotations

from typing import TYPE_CHECKING

import daiquiri
from humanfriendly.text import pluralize

if TYPE_CHECKING:
    from collections.abc import Iterable

    from dbnomics_data_model import DatasetCode, ProviderCode
    from dbnomics_data_model.storage.adapters.filesystem import FileSystemStorage

    from dbnomics_solr.dbnomics_solr_client import DBnomicsSolrClient

__all__ = ["search_extra_datasets"]


logger = daiquiri.getLogger(__name__)


def search_extra_datasets(
    provider_code: ProviderCode,
    *,
    dbnomics_solr_client: DBnomicsSolrClient,
    storage: FileSystemStorage,
    storage_dataset_codes: Iterable[DatasetCode] | None = None,
) -> set[DatasetCode]:
    """Search the extra datasets related to that provider."""
    extra_dataset_codes = dbnomics_solr_client.search_extra_datasets(
        provider_code, storage=storage, storage_dataset_codes=storage_dataset_codes
    )
    if len(extra_dataset_codes) == 0:
        logger.debug("No extra datasets were found for that provider", provider_code=provider_code)
    else:
        logger.debug(
            "Found %s for that provider",
            pluralize(len(extra_dataset_codes), "extra dataset"),
            provider_code=provider_code,
        )
    return extra_dataset_codes

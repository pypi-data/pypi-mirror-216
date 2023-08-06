"""Domain-level service to delete data related to a dataset."""

from __future__ import annotations

from typing import TYPE_CHECKING

import daiquiri

from dbnomics_solr import services

if TYPE_CHECKING:
    from collections.abc import Iterable

    from dbnomics_data_model import DatasetCode, ProviderCode
    from dbnomics_data_model.storage.adapters.filesystem import FileSystemStorage

    from dbnomics_solr.dbnomics_solr_client import DBnomicsSolrClient

__all__ = ["delete_extra_datasets"]


logger = daiquiri.getLogger(__name__)


def delete_extra_datasets(
    provider_code: ProviderCode,
    *,
    dbnomics_solr_client: DBnomicsSolrClient,
    storage: FileSystemStorage,
    storage_dataset_codes: Iterable[DatasetCode] | None = None,
    update_top_level_counts: bool = True,
) -> None:
    """Delete the extra datasets related to that provider."""
    extra_dataset_codes = services.search_extra_datasets(
        provider_code,
        dbnomics_solr_client=dbnomics_solr_client,
        storage=storage,
        storage_dataset_codes=storage_dataset_codes,
    )
    for dataset_code in extra_dataset_codes:
        dataset_id = f"{provider_code}/{dataset_code}"
        logger.info("Deleting the extra dataset", dataset_id=dataset_id)
        dbnomics_solr_client.delete_dataset_docs(provider_code, dataset_code)

    if update_top_level_counts:
        services.update_top_level_counts(commit=False, dbnomics_solr_client=dbnomics_solr_client)

    dbnomics_solr_client.commit()

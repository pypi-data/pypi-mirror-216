"""Domain-level service to delete data related to a dataset."""

from __future__ import annotations

from typing import TYPE_CHECKING

import daiquiri

from dbnomics_solr import services

if TYPE_CHECKING:
    from dbnomics_data_model import DatasetCode, ProviderCode

    from dbnomics_solr.dbnomics_solr_client import DBnomicsSolrClient

__all__ = ["delete_dataset_docs"]


logger = daiquiri.getLogger(__name__)


def delete_dataset_docs(
    provider_code: ProviderCode, dataset_code: DatasetCode, *, dbnomics_solr_client: DBnomicsSolrClient
) -> None:
    """Delete Solr documents related to that dataset."""
    dataset_id = f"{provider_code}/{dataset_code}"

    results = dbnomics_solr_client.search_dataset_docs(provider_code, dataset_code)
    if results.hit_sum() == 0:
        logger.warning(
            "No documents related to that dataset were found, but sending the delete requests anyway.",
            dataset_id=dataset_id,
        )
    else:
        logger.debug("Found %s", results.format_hits_by_type())

    logger.info("Deleting all the Solr documents related to that dataset...", dataset_id=dataset_id)
    dbnomics_solr_client.delete_dataset_docs(provider_code, dataset_code)

    services.update_top_level_counts(commit=False, dbnomics_solr_client=dbnomics_solr_client)

    dbnomics_solr_client.commit()
    logger.info("All the Solr documents related to that dataset were deleted", dataset_id=dataset_id)

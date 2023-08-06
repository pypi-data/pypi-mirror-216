"""Domain-level service to delete data related to a provider."""

from __future__ import annotations

from typing import TYPE_CHECKING

import daiquiri

from dbnomics_solr import services
from dbnomics_solr.errors import InvalidSolrDocument, ProviderNotFound

if TYPE_CHECKING:
    from dbnomics_data_model import ProviderCode

    from dbnomics_solr.dbnomics_solr_client import DBnomicsSolrClient

__all__ = ["delete_provider_docs"]


logger = daiquiri.getLogger(__name__)


def delete_provider_docs(
    *,
    provider_code: ProviderCode | None = None,
    provider_slug: str | None = None,
    dbnomics_solr_client: DBnomicsSolrClient,
) -> None:
    """Delete Solr documents related to a provider identified by its code or its slug."""
    if provider_code is None and provider_slug is None:
        msg = "Either provider_code or provider_slug must be specified"
        raise ValueError(msg)

    if provider_slug is not None:
        logger.debug("Finding the provider code from the provider slug...", provider_slug=provider_slug)
        assert provider_code is None, provider_code
        try:
            provider_code = dbnomics_solr_client.find_provider_code_from_slug(provider_slug)
        except InvalidSolrDocument:
            logger.exception(
                "Could not find the provider code in the Solr document for the provider, skipping deletion",
                provider_slug=provider_slug,
            )
            return
        except ProviderNotFound:
            logger.exception(
                "Could not find the Solr document for the provider, skipping deletion", provider_slug=provider_slug
            )
            return

    assert provider_code is not None

    results = dbnomics_solr_client.search_provider_docs(provider_code)
    if results.hit_sum() == 0:
        logger.warning(
            "No documents related to that provider were found, but sending the delete requests anyway.",
            provider_code=provider_code,
        )
    else:
        logger.debug("Found %s", results.format_hits_by_type())

    logger.info("Deleting all the Solr documents related to that provider...", provider_code=provider_code)
    dbnomics_solr_client.delete_provider_docs(provider_code)

    services.update_top_level_counts(commit=False, dbnomics_solr_client=dbnomics_solr_client)

    dbnomics_solr_client.commit()
    logger.info("All the Solr documents related to that provider were deleted", provider_code=provider_code)

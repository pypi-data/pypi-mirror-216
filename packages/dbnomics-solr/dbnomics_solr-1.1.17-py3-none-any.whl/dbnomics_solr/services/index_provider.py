"""Domain-level service to index data related to a provider."""

from __future__ import annotations

import time
from datetime import datetime, timezone
from typing import TYPE_CHECKING

import daiquiri
from dbnomics_data_model.storage.errors import ProviderMetadataNotFound
from humanfriendly import format_timespan
from humanfriendly.text import pluralize

from dbnomics_solr import services
from dbnomics_solr.dbnomics_solr_client import DBnomicsSolrClient, format_date_for_solr
from dbnomics_solr.errors import DatasetAlreadyIndexed

if TYPE_CHECKING:
    from dbnomics_data_model import DatasetCode
    from dbnomics_data_model.storage.adapters.filesystem import FileSystemStorage

__all__ = ["index_provider"]


logger = daiquiri.getLogger(__name__)


def index_provider(
    *,
    delete_obsolete_series: bool,
    delete_extra_datasets: bool,
    dirhash_jobs: int,
    fail_fast: bool,
    force: bool,
    solr_url: str,
    dataset_codes: list[DatasetCode] | None = None,
    limit: int | None = None,
    solr_timeout: int = 60,
    storage: FileSystemStorage,
    storage_dataset_codes: list[DatasetCode] | None = None,
) -> None:
    """Index data from a provider storage."""
    indexed_at = datetime.now(timezone.utc)
    logger.debug("Using indexed_at %r for all the Solr documents", format_date_for_solr(indexed_at))

    dbnomics_solr_client = DBnomicsSolrClient(
        solr_url,
        dirhash_jobs=dirhash_jobs,
        indexed_at=indexed_at,
        retry_num_attempts=1 if fail_fast else None,
        timeout=solr_timeout,
    )

    # Prepare provider

    try:
        provider_metadata = storage.load_provider_metadata()
    except ProviderMetadataNotFound:
        logger.debug("Provider metadata was not found")
        return

    provider_code = provider_metadata.code
    logger.debug("About to index data for provider %r", provider_code)

    logger.info("Indexing provider metadata...", provider_code=provider_code)
    dbnomics_solr_client.index_provider(provider_metadata)
    dbnomics_solr_client.commit()
    logger.info("Provider metadata indexed", provider_code=provider_code)

    # Index datasets

    if storage_dataset_codes is None:
        storage_dataset_codes = sorted(storage.iter_dataset_codes(on_error="log"))

    if dataset_codes is None:
        dataset_codes = storage_dataset_codes

    if not dataset_codes:
        logger.info("No dataset to process for provider %r", provider_code)
        return

    if limit is not None:
        logger.debug("About to index %d/%d datasets due to the limit option...", limit, len(dataset_codes))
        dataset_codes = dataset_codes[:limit]
    else:
        logger.debug("About to index all the %d datasets...", len(dataset_codes))

    successful_dataset_codes = set()
    skipped_dataset_codes = set()

    for dataset_index, dataset_code in enumerate(dataset_codes, start=1):
        t0 = time.time()
        logger.debug("About to index dataset %r (%d/%d)", dataset_code, dataset_index, len(dataset_codes))
        try:
            dbnomics_solr_client.index_dataset(
                dataset_code, storage=storage, provider_metadata=provider_metadata, force=force
            )
        except DatasetAlreadyIndexed as exc:
            logger.debug(
                "Dataset %r (%d/%d) is already indexed with the directory hash %r "
                "and was not updated since previous indexation, skipping dataset",
                exc.dataset_code,
                dataset_index,
                len(dataset_codes),
                exc.dir_hash,
            )
            continue
        except Exception:
            if fail_fast:
                raise
            logger.exception("Error indexing dataset %r, skipping dataset", dataset_code)
            skipped_dataset_codes.add(dataset_code)
            continue
        else:
            successful_dataset_codes.add(dataset_code)

        dbnomics_solr_client.commit()
        logger.info(
            "Dataset %r (%d/%d) was indexed in %s",
            dataset_code,
            dataset_index,
            len(dataset_codes),
            format_timespan(time.time() - t0),
        )

    if delete_obsolete_series:
        if successful_dataset_codes:
            logger.info(
                "Deleting the obsolete series of the %d successfully indexed datasets...",
                len(successful_dataset_codes),
                provider_code=provider_code,
            )
            dbnomics_solr_client.delete_obsolete_series(provider_code, sorted(successful_dataset_codes))
            dbnomics_solr_client.commit()
            logger.info(
                "The obsolete series of the %d successfully indexed datasets were deleted",
                len(successful_dataset_codes),
                provider_code=provider_code,
            )
        else:
            logger.debug("No dataset was indexed, no need to delete obsolete series")

    if delete_extra_datasets:
        services.delete_extra_datasets(
            provider_code,
            dbnomics_solr_client=dbnomics_solr_client,
            storage=storage,
            storage_dataset_codes=storage_dataset_codes,
            update_top_level_counts=False,
        )

    if skipped_dataset_codes:
        logger.error(
            "Summary stats: %s skipped during the indexation process: %r",
            pluralize(len(skipped_dataset_codes), singular="dataset was", plural="datasets were"),
            sorted(skipped_dataset_codes),
            provider_code=provider_code,
        )

    services.update_top_level_counts(dbnomics_solr_client=dbnomics_solr_client)

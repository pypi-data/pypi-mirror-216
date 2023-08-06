# noqa: I002

"""Index DBnomics data into Apache Solr for full-text and faceted search."""

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import daiquiri
import typer
from dbnomics_data_model import DatasetCode, ProviderCode
from dbnomics_data_model.storage.adapters.filesystem import FileSystemStorage, FileSystemStoragePool
from dotenv import load_dotenv

from . import services
from .cli_utils import list_callback
from .dbnomics_solr_client import DBnomicsSolrClient

INDEXATION = "INDEXATION"
DELETION = "DELETION"
GIT_MODE_TREE_STR = "040000"


@dataclass
class AppArgs:
    """Script arguments common to all commands."""

    solr_timeout: int
    solr_url: str


app = typer.Typer()
app_args: Optional[AppArgs] = None


logger = daiquiri.getLogger(__name__)

load_dotenv()


@app.callback(context_settings={"help_option_names": ["-h", "--help"]})
def main(
    debug: bool = typer.Option(False, help="Display DEBUG log messages."),
    solr_timeout: int = typer.Option(60, envvar="SOLR_TIMEOUT"),
    solr_url: str = typer.Option("http://127.0.0.1:8983/solr/dbnomics", envvar="SOLR_URL"),
) -> None:
    """Index DBnomics data using Apache Solr."""
    global app_args  # noqa: PLW0603
    app_args = AppArgs(solr_timeout=solr_timeout, solr_url=solr_url)

    daiquiri.setup()
    daiquiri.set_default_log_levels([(__package__, logging.DEBUG if debug else logging.INFO)])

    logger.debug("Using app args: %r", app_args)


@app.command()
def delete_dataset(
    provider_code: ProviderCode = typer.Option(..., "--provider-code"),
    dataset_code: DatasetCode = typer.Option(..., "--dataset-code"),
) -> None:
    """Delete all the documents related to that dataset.

    This includes the document representing the dataset, but also all the ones representing the series of that dataset.
    """
    assert app_args is not None  # it is set by "main" function
    dbnomics_solr_client = DBnomicsSolrClient(app_args.solr_url, timeout=app_args.solr_timeout)
    services.delete_dataset_docs(provider_code, dataset_code, dbnomics_solr_client=dbnomics_solr_client)


@app.command()
def delete_extra_datasets(provider_code: ProviderCode, storage_dir: Path = typer.Option(...)) -> None:
    """Delete the extra datasets related to that provider (those that are in Solr but not in the storage)."""
    assert app_args is not None  # it is set by "main" function
    dbnomics_solr_client = DBnomicsSolrClient(app_args.solr_url, timeout=app_args.solr_timeout)
    storage = FileSystemStorage(storage_dir)
    services.delete_extra_datasets(provider_code, dbnomics_solr_client=dbnomics_solr_client, storage=storage)


@app.command()
def delete_provider(
    provider_code: Optional[ProviderCode] = typer.Option(None, "--provider-code"),
    provider_slug: Optional[str] = typer.Option(None, "--provider-slug"),
) -> None:
    """Delete all the documents related to that provider.

    This includes the document representing that provider, but also the one representing the datasets of that provider,
    and the ones representing the series of the datasets of that provider.
    """
    assert app_args is not None  # it is set by "main" function

    if bool(provider_code) == bool(provider_slug):
        typer.echo("one of 'code' or 'slug' options must be provided")
        raise typer.Abort

    dbnomics_solr_client = DBnomicsSolrClient(app_args.solr_url, timeout=app_args.solr_timeout)

    if provider_code is not None:
        services.delete_provider_docs(provider_code=provider_code, dbnomics_solr_client=dbnomics_solr_client)
    elif provider_slug is not None:
        services.delete_provider_docs(provider_slug=provider_slug, dbnomics_solr_client=dbnomics_solr_client)


@app.command()
def search_datasets(provider_code: ProviderCode) -> None:
    """Search the datasets related to that provider."""
    assert app_args is not None  # it is set by "main" function
    dbnomics_solr_client = DBnomicsSolrClient(app_args.solr_url, timeout=app_args.solr_timeout)
    results = services.search_provider_datasets(provider_code, dbnomics_solr_client=dbnomics_solr_client)
    for result in results:
        typer.echo(result["code"])


@app.command()
def search_extra_datasets(provider_code: ProviderCode, storage_dir: Path = typer.Option(...)) -> None:
    """Search the extra datasets related to that provider (those that are in Solr but not in the storage)."""
    assert app_args is not None  # it is set by "main" function
    dbnomics_solr_client = DBnomicsSolrClient(app_args.solr_url, timeout=app_args.solr_timeout)
    storage = FileSystemStorage(storage_dir)
    extra_dataset_codes = services.search_extra_datasets(
        provider_code, dbnomics_solr_client=dbnomics_solr_client, storage=storage
    )
    for dataset_code in sorted(extra_dataset_codes):
        typer.echo(dataset_code)


@app.command()
def index_providers(
    storage_base_dir: Path,
    delete_extra_datasets: bool = typer.Option(
        False,
        envvar="DELETE_EXTRA_DATASETS",
        help="After indexation, delete datasets that are in Solr but not in the storage.",
    ),
    delete_obsolete_series: bool = typer.Option(
        False,
        envvar="DELETE_OBSOLETE_SERIES",
        help="After indexation, delete series that were not created or updated.",
    ),
    dirhash_jobs: int = typer.Option(
        1, envvar="DIRHASH_JOBS", help="The number of processes to use when computing a dirhash."
    ),
    fail_fast: bool = typer.Option(False, envvar="FAIL_FAST", help="Disable retry mechanism."),
    force: bool = typer.Option(False, envvar="FORCE", help="Always index data (ignore dir hashes)."),
    limit: Optional[int] = typer.Option(None, envvar="LIMIT", help="Index a maximum number of datasets per provider."),
) -> None:
    """Index many providers to Solr from storage_base_dir.

    In storage_base_dir each child directory is considered as the storage directory
    of a provider.
    """
    assert app_args is not None  # it is set by "main" function

    storage_pool = FileSystemStoragePool(storage_base_dir)
    for storage in storage_pool.iter_storages():
        services.index_provider(
            delete_extra_datasets=delete_extra_datasets,
            delete_obsolete_series=delete_obsolete_series,
            dirhash_jobs=dirhash_jobs,
            fail_fast=fail_fast,
            force=force,
            limit=limit,
            solr_timeout=app_args.solr_timeout,
            solr_url=app_args.solr_url,
            storage=storage,
        )


@app.command()
def index_provider(
    storage_dir: Path,
    datasets: list[DatasetCode] = typer.Option(
        [], "--datasets", callback=list_callback, envvar="DATASETS", help="Index only the given datasets."
    ),
    delete_extra_datasets: bool = typer.Option(
        False,
        envvar="DELETE_EXTRA_DATASETS",
        help="After indexation, delete datasets that are in Solr but not in the storage.",
    ),
    delete_obsolete_series: bool = typer.Option(
        False,
        envvar="DELETE_OBSOLETE_SERIES",
        help="After indexation, delete series that were not created or updated.",
    ),
    dirhash_jobs: int = typer.Option(
        1, envvar="DIRHASH_JOBS", help="The number of processes to use when computing a dirhash."
    ),
    excluded_datasets: list[DatasetCode] = typer.Option(
        [],
        "--exclude-datasets",
        callback=list_callback,
        envvar="EXCLUDE_DATASETS",
        help="Do not index the given datasets.",
    ),
    fail_fast: bool = typer.Option(False, envvar="FAIL_FAST", help="Disable retry mechanism."),
    force: bool = typer.Option(False, envvar="FORCE", help="Always index data (ignore dir hashes)."),
    limit: Optional[int] = typer.Option(None, envvar="LIMIT", help="Index a maximum number of datasets."),
    start_from: DatasetCode = typer.Option(None, help="Start indexing from dataset code."),
) -> None:
    """Index a single provider to Solr from storage_dir."""
    assert app_args is not None  # it is set by "main" function

    if limit is not None and limit <= 0:
        typer.echo("limit option must be strictly positive")
        raise typer.Abort

    if not storage_dir.is_dir():
        typer.echo(f"storage_dir {storage_dir!s} not found")
        raise typer.Abort

    storage = FileSystemStorage(storage_dir)
    storage_dataset_codes = sorted(storage.iter_dataset_codes(on_error="log"))
    dataset_codes = [
        dataset_code
        for dataset_code in storage_dataset_codes
        if is_desired_dataset(dataset_code, datasets, excluded_datasets, start_from)
    ]

    services.index_provider(
        dataset_codes=dataset_codes,
        delete_extra_datasets=delete_extra_datasets,
        delete_obsolete_series=delete_obsolete_series,
        dirhash_jobs=dirhash_jobs,
        fail_fast=fail_fast,
        force=force,
        limit=limit,
        solr_timeout=app_args.solr_timeout,
        solr_url=app_args.solr_url,
        storage=storage,
        storage_dataset_codes=storage_dataset_codes,
    )


@app.command()
def update_top_level_counts() -> None:
    """Update the counts of providers, datasets and series."""
    assert app_args is not None  # it is set by "main" function

    dbnomics_solr_client = DBnomicsSolrClient(app_args.solr_url, timeout=app_args.solr_timeout)

    services.update_top_level_counts(dbnomics_solr_client=dbnomics_solr_client)


def is_desired_dataset(
    dataset_code: DatasetCode,
    datasets: list[DatasetCode],
    excluded_datasets: list[DatasetCode],
    start_from: DatasetCode,
) -> bool:
    """Apply script arguments to detemine if a dataset has to be indexed."""
    if datasets and dataset_code not in datasets:
        logger.debug("Skipping dataset %r because it is not mentioned by the --datasets option", dataset_code)
        return False
    if excluded_datasets and dataset_code in excluded_datasets:
        logger.debug("Skipping dataset %r because it is mentioned by the --exclude-datasets option", dataset_code)
        return False
    if start_from is not None and dataset_code < start_from:
        logger.debug("Skipping dataset %r because of the --start-from option", dataset_code)
        return False
    return True


if __name__ == "__main__":
    app()

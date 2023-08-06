from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from dbnomics_data_model import DatasetCode, ProviderCode
    from solrq import Q

    from dbnomics_solr.types import SolrDoc

__all__ = [
    "DatasetAlreadyIndexed",
    "DatasetNotFound",
    "DBnomicsSolrException",
    "DuplicateDocuments",
    "IndexationError",
    "InvalidSolrDocument",
    "ProviderNotFound",
]


class DBnomicsSolrException(Exception):
    pass


class DatasetAlreadyIndexed(DBnomicsSolrException):
    def __init__(self, provider_code: ProviderCode, dataset_code: DatasetCode, *, dir_hash: str) -> None:
        dataset_id = f"{provider_code}/{dataset_code}"
        message = f"The dataset {dataset_id!r} is already indexed (dir_hash: {dir_hash})"
        super().__init__(message)
        self.provider_code = provider_code
        self.dataset_code = dataset_code
        self.dir_hash = dir_hash


class DatasetNotFound(DBnomicsSolrException):
    def __init__(self, provider_code: ProviderCode, dataset_code: DatasetCode) -> None:
        dataset_id = f"{provider_code}/{dataset_code}"
        message = f"The dataset {dataset_id!r} was not found"
        super().__init__(message)
        self.provider_code = provider_code
        self.dataset_code = dataset_code


class DuplicateDocuments(DBnomicsSolrException):
    def __init__(self, *, query: Q, hits: int) -> None:
        message = f"The query {query!r} was expected to return at most one document but it returned {hits}"
        super().__init__(message)
        self.query = query
        self.hits = hits


class InvalidSolrDocument(DBnomicsSolrException):
    def __init__(self, message: str = "Invalid Solr document", *, solr_document: SolrDoc) -> None:
        super().__init__(message)
        self.solr_document = solr_document


class ProviderNotFound(DBnomicsSolrException):
    def __init__(self, provider_slug: str) -> None:
        message = f"The provider {provider_slug!r} was not found"
        super().__init__(message)
        self.provider_slug = provider_slug


class IndexationError(DBnomicsSolrException):
    def __init__(self, error: dict[str, Any] | None = None) -> None:
        message = f"Indexation error: {error!r}"
        super().__init__(message)
        self.error = error

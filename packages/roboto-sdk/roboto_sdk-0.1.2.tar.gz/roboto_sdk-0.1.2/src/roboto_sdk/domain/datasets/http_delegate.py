import json
from typing import Any
import urllib.parse

from ...http import HttpClient
from ...pagination import PaginatedList
from ...serde import pydantic_jsonable_dict
from ..files import FileRecord
from .delegate import (
    AccessMode,
    Credentials,
    DatasetDelegate,
)
from .http_resources import CreateDatasetRequest
from .record import (
    Administrator,
    DatasetRecord,
    StorageLocation,
)


class DatasetHttpDelegate(DatasetDelegate):
    __http_client: HttpClient
    __roboto_service_base_url: str

    def __init__(self, roboto_service_base_url: str, http_client: HttpClient) -> None:
        super().__init__()
        self.__http_client = http_client
        self.__roboto_service_base_url = roboto_service_base_url

    def create_dataset(
        self,
        administrator: Administrator = Administrator.Roboto,
        metadata: dict[str, Any] | None = None,
        storage_location: StorageLocation = StorageLocation.S3,
        tags: list[str] | None = None,
        tenant_id: str | None = None,
        created_by: str | None = None,
    ) -> DatasetRecord:
        """
        Create a new dataset.

        `tenant_id` and `created_by` are ignored, as both are determined server-side by the identity of the caller.
        """
        url = f"{self.__roboto_service_base_url}/v1/datasets"
        request_body = CreateDatasetRequest(
            administrator=administrator,
            metadata=metadata if metadata is not None else {},
            storage_location=storage_location,
            tags=tags if tags is not None else [],
        )
        response = self.__http_client.post(
            url,
            data=pydantic_jsonable_dict(request_body),
            headers={"Content-Type": "application/json"},
        )
        return DatasetRecord.parse_obj(response.from_json(json_path=["data"]))

    def get_dataset_by_primary_key(
        self,
        dataset_id: str,
        tenant_id: str | None = None,
    ) -> DatasetRecord:
        """
        Get a dataset by its primary key (tenant_id, dataset_id)

        `tenant_id` is ignored, as it is determined server-side by the identity of the caller.
        """
        url = f"{self.__roboto_service_base_url}/v1/datasets/{dataset_id}"
        response = self.__http_client.get(url)
        return DatasetRecord.parse_obj(response.from_json(json_path=["data"]))

    def get_temporary_credentials(
        self, record: DatasetRecord, mode: AccessMode, caller: str | None = None
    ) -> Credentials:
        """
        Get temporary credentials to access a dataset.

        `caller` is ignored, as it is determined server-side by the identity of the caller.
        """
        query_params = {"mode": mode.value}
        encoded_qs = urllib.parse.urlencode(query_params)
        url = f"{self.__roboto_service_base_url}/v1/datasets/{record.id}/credentials?{encoded_qs}"
        response = self.__http_client.get(url)
        return Credentials.parse_obj(response.from_json(json_path=["data"]))

    def list_files(
        self,
        dataset_id: str,
        tenant_id: str | None = None,
        page_token: dict[str, str] | None = None,
    ) -> PaginatedList[FileRecord]:
        """
        List files associated with dataset.

        Files are associated with datasets in an eventually-consistent manner,
        so there will likely be delay between a file being uploaded and it appearing in this list.

        `tenant_id` is ignored, as it is determined server-side by the identity of the caller.
        """
        url = f"{self.__roboto_service_base_url}/v1/datasets/{dataset_id}/files"
        if page_token:
            query_str = urllib.parse.urlencode(page_token)
            url = f"{url}?{query_str}"
        response = self.__http_client.get(url)
        unmarshalled = response.from_json(json_path=["data"])
        return PaginatedList(
            items=[FileRecord.parse_obj(file) for file in unmarshalled["items"]],
            next_token=unmarshalled["next_token"],
        )

    def query_datasets(
        self, filters: dict[str, Any], page_token: dict[str, str] | None = None
    ) -> PaginatedList[DatasetRecord]:
        if page_token:
            filters["page_token"] = page_token

        safe_filters = json.loads(json.dumps(filters))
        url = f"{self.__roboto_service_base_url}/v1/datasets/query"
        res = self.__http_client.post(
            url, data=safe_filters, headers={"Content-Type": "application/json"}
        )
        unmarshalled = res.from_json(json_path=["data"])
        return PaginatedList(
            items=[
                DatasetRecord.parse_obj(dataset) for dataset in unmarshalled["items"]
            ],
            next_token=unmarshalled["next_token"],
        )

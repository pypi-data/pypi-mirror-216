import json
from typing import Any

from ...http import HttpClient
from ...logging import default_logger
from ...model.actions import (
    InvocationDataSourceType,
    InvocationDelegate,
    InvocationRecord,
    InvocationSource,
    InvocationStatus,
)
from ...pagination import PaginatedList
from ...serde import pydantic_jsonable_dict
from .invocation_http_resources import (
    CreateInvocationRequest,
)

logger = default_logger()


class InvocationHttpDelegate(InvocationDelegate):
    """
    Use in any context that does not have direct database access.
    """

    __http_client: HttpClient
    __roboto_service_base_url: str

    def __init__(self, roboto_service_base_url: str, http_client: HttpClient) -> None:
        super().__init__()
        self.__http_client = http_client
        self.__roboto_service_base_url = roboto_service_base_url

    def create_invocation(
        self,
        action_name: str,
        input_data: list[str],
        data_source_id: str,
        data_source_type: InvocationDataSourceType,
        invocation_source: InvocationSource,
        invocation_source_id: str | None = None,
        tenant_id: str | None = None,
    ) -> InvocationRecord:
        """
        `tenant_id` and `invocation_source_id` are ignored client-side; they are determined server-side.
        """
        url = f"{self.__roboto_service_base_url}/v1/actions/{action_name}/invoke"
        request_body = CreateInvocationRequest(
            input_data=input_data,
            data_source_id=data_source_id,
            data_source_type=data_source_type,
            invocation_source=invocation_source,
            invocation_source_id=invocation_source_id,
        )
        response = self.__http_client.post(
            url,
            data=pydantic_jsonable_dict(request_body, exclude_none=True),
            headers={"Content-Type": "application/json"},
        )
        return InvocationRecord.parse_obj(response.from_json(json_path=["data"]))

    def get_by_id(self, invocation_id: str) -> InvocationRecord:
        """Get an Invocation by ID"""
        raise NotImplementedError("get_by_id")

    def update_invocation_status(
        self,
        invocation: InvocationRecord,
        status: InvocationStatus,
        detail: str | None = None,
    ) -> InvocationRecord:
        url = f"{self.__roboto_service_base_url}/v1/actions/{invocation.action_name}/invoke/{invocation.id}/status"
        response = self.__http_client.post(
            url,
            data={"status": status.value, "detail": detail},
            headers={"Content-Type": "application/json"},
        )
        return InvocationRecord.parse_obj(response.from_json(json_path=["data"]))

    def query_invocations(
        self, filters: dict[str, Any], page_token: dict[str, str] | None = None
    ) -> PaginatedList[InvocationRecord]:
        if page_token:
            filters["page_token"] = page_token

        safe_filters = json.loads(json.dumps(filters))
        url = f"{self.__roboto_service_base_url}/v1/actions/invocations/query"
        res = self.__http_client.post(
            url, data=safe_filters, headers={"Content-Type": "application/json"}
        )
        unmarshalled = res.from_json(json_path=["data"])
        return PaginatedList(
            items=[
                InvocationRecord.parse_obj(dataset) for dataset in unmarshalled["items"]
            ],
            next_token=unmarshalled["next_token"],
        )

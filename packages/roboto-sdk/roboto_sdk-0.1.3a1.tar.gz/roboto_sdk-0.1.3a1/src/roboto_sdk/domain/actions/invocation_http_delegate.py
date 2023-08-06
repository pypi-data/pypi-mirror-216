import json
from typing import Any

from ...http import HttpClient
from ...logging import default_logger
from ...pagination import PaginatedList
from ...serde import pydantic_jsonable_dict
from .invocation_delegate import (
    InvocationDelegate,
)
from .invocation_http_resources import (
    CreateInvocationRequest,
    SetLogsLocationRequest,
)
from .invocation_record import (
    InvocationDataSourceType,
    InvocationRecord,
    InvocationSource,
    InvocationStatus,
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
        headers = {"Content-Type": "application/json"}
        if tenant_id:
            headers["X-Roboto-Org-Id"] = tenant_id
        response = self.__http_client.post(
            url,
            data=pydantic_jsonable_dict(request_body, exclude_none=True),
            headers=headers,
        )
        return InvocationRecord.parse_obj(response.from_json(json_path=["data"]))

    def get_by_id(
        self, invocation_id: str, org_id: str | None = None
    ) -> InvocationRecord:
        url = f"{self.__roboto_service_base_url}/v1/actions/invocations/{invocation_id}"
        headers = {}
        if org_id:
            headers["X-Roboto-Org-Id"] = org_id
        response = self.__http_client.get(url, headers=headers)
        return InvocationRecord.parse_obj(response.from_json(json_path=["data"]))

    def set_logs_location(
        self, record: InvocationRecord, bucket: str, prefix: str
    ) -> InvocationRecord:
        url = (
            f"{self.__roboto_service_base_url}/v1/actions/invocations/{record.id}/logs"
        )
        headers = {
            "Content-Type": "application/json",
            "X-Roboto-Org-Id": record.tenant_id,
        }
        request_body = SetLogsLocationRequest(bucket=bucket, prefix=prefix)
        response = self.__http_client.patch(
            url,
            data=pydantic_jsonable_dict(request_body, exclude_none=True),
            headers=headers,
        )
        return InvocationRecord.parse_obj(response.from_json(json_path=["data"]))

    def update_invocation_status(
        self,
        invocation: InvocationRecord,
        status: InvocationStatus,
        detail: str | None = None,
    ) -> InvocationRecord:
        url = f"{self.__roboto_service_base_url}/v1/actions/invocations/{invocation.id}/status"
        headers = {
            "Content-Type": "application/json",
            "X-Roboto-Org-Id": invocation.tenant_id,
        }
        response = self.__http_client.post(
            url,
            data={"status": status.value, "detail": detail},
            headers=headers,
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

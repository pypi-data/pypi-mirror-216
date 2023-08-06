import http
import json
from typing import Any

from ...http import ClientError, HttpClient
from ...logging import default_logger
from ...pagination import PaginatedList
from ...serde import pydantic_jsonable_dict
from .action_delegate import (
    ActionDelegate,
    ContainerCredentials,
    UpdateCondition,
)
from .action_http_resources import (
    CreateActionRequest,
    UpdateActionRequest,
)
from .action_record import ActionRecord
from .error import (
    ActionUpdateConditionCheckFailure,
)

logger = default_logger()


class ActionHttpDelegate(ActionDelegate):
    """
    Use in any context that does not have direct database access.
    """

    __http_client: HttpClient
    __roboto_service_base_url: str

    def __init__(self, roboto_service_base_url: str, http_client: HttpClient) -> None:
        super().__init__()
        self.__http_client = http_client
        self.__roboto_service_base_url = roboto_service_base_url

    def create_action(
        self,
        name: str,
        tenant_id: str | None = None,
        created_by: str | None = None,
        description: str | None = None,
        metadata: dict[str, Any] | None = None,
        tags: list[str] | None = None,
    ) -> ActionRecord:
        """
        `tenant_id` and `created_by` are ignored, as both are determined server-side by the identity of the caller.
        """
        url = f"{self.__roboto_service_base_url}/v1/actions"
        request_body = CreateActionRequest(
            name=name,
            description=description,
            metadata=metadata,
            tags=tags,
        )
        response = self.__http_client.post(
            url,
            data=pydantic_jsonable_dict(request_body, exclude_none=True),
            headers={"Content-Type": "application/json", "X-Roboto-Org-Id": tenant_id},
        )
        return ActionRecord.parse_obj(response.from_json(json_path=["data"]))

    def get_action_by_primary_key(
        self, name: str, tenant_id: str | None = None
    ) -> ActionRecord:
        """
        `tenant_id` is ignored, as it is determined server-side by the identity of the caller.
        """
        url = f"{self.__roboto_service_base_url}/v1/actions/{name}"
        headers = {}
        if tenant_id:
            headers["X-Roboto-Org-Id"] = tenant_id
        res = self.__http_client.get(url, headers=headers)
        return ActionRecord.parse_obj(res.from_json(json_path=["data"]))

    def register_container(
        self,
        record: ActionRecord,
        image_name: str,
        image_tag: str,
        caller: str | None = None,
    ) -> tuple[str, str]:
        url = f"{self.__roboto_service_base_url}/v1/actions/{record.name}/container"
        data = {
            "image_name": image_name,
            "image_tag": image_tag,
        }

        res = self.__http_client.put(
            url, data=data, headers={"Content-Type": "application/json"}
        )
        parsed_res = res.from_json(json_path=["data"])
        return (parsed_res["repository_uri"], parsed_res["image_uri"])

    def get_temp_container_credentials(
        self,
        record: ActionRecord,
        caller: str | None = None,
    ) -> ContainerCredentials:
        url = f"{self.__roboto_service_base_url}/v1/actions/{record.name}/container/credentials"
        res = self.__http_client.get(url)
        return ContainerCredentials.parse_obj(res.from_json(json_path=["data"]))

    def query_actions(
        self, filters: dict[str, Any], page_token: dict[str, str] | None = None
    ) -> PaginatedList[ActionRecord]:
        if page_token:
            filters["page_token"] = page_token

        safe_filters = json.loads(json.dumps(filters))
        url = f"{self.__roboto_service_base_url}/v1/actions/query"
        res = self.__http_client.post(
            url, data=safe_filters, headers={"Content-Type": "application/json"}
        )
        unmarshalled = res.from_json(json_path=["data"])
        return PaginatedList(
            items=[
                ActionRecord.parse_obj(dataset) for dataset in unmarshalled["items"]
            ],
            next_token=unmarshalled["next_token"],
        )

    def update(
        self,
        record: ActionRecord,
        updates: dict[str, Any],
        conditions: list[UpdateCondition] | None,
        tenant_id: str | None = None,
    ) -> ActionRecord:
        """
        For most requests, `tenant_id` is ignored, as it is determined server-side by the identity of the caller.
        It is only ever user when the caller is a Roboto service user.
        """
        url = f"{self.__roboto_service_base_url}/v1/actions/{record.name}"
        payload = UpdateActionRequest(
            updates=updates,
            conditions=conditions if conditions is not None else [],
            tenant_id=tenant_id,
        )
        try:
            res = self.__http_client.patch(url, data=payload.dict())
            return ActionRecord.parse_obj(res.from_json(json_path=["data"]))
        except ClientError as exc:
            if exc.status == http.HTTPStatus.CONFLICT:
                raise ActionUpdateConditionCheckFailure(exc.msg) from None
            raise

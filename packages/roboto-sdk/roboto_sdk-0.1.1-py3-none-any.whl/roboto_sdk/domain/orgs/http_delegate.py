#  Copyright (c) 2023 Roboto Technologies, Inc.


from ...http import (
    ORG_OVERRIDE_HEADER,
    USER_OVERRIDE_HEADER,
    HttpClient,
)
from ...serde import pydantic_jsonable_dict
from .delegate import OrgDelegate
from .http_resources import CreateOrgRequest
from .record import (
    OrgRecord,
    OrgRoleRecord,
    OrgType,
)


class OrgHttpDelegate(OrgDelegate):
    __http_client: HttpClient

    def __init__(self, http_client: HttpClient):
        super().__init__()
        self.__http_client = http_client

    def create_org(
        self, creator_user_id: str | None, name: str, org_type: OrgType
    ) -> OrgRecord:
        url = self.__http_client.url("v1/orgs")
        headers = {"Content-Type": "application/json"}

        if creator_user_id is not None:
            headers[USER_OVERRIDE_HEADER] = creator_user_id

        request_body = CreateOrgRequest(name=name, org_type=org_type)
        response = self.__http_client.post(
            url=url, headers=headers, data=pydantic_jsonable_dict(request_body)
        )
        return OrgRecord.parse_obj(response.from_json(json_path=["data"]))

    def orgs_for_user(self, user_id: str | None) -> list[OrgRecord]:
        url = self.__http_client.url("v1/orgs/list")
        response = self.__http_client.get(url=url)
        return [
            OrgRecord.parse_obj(record)
            for record in response.from_json(json_path=["data"])
        ]

    def org_roles_for_user(self, user_id: str | None) -> list[OrgRoleRecord]:
        url = self.__http_client.url("v1/orgs/roles")
        response = self.__http_client.get(url=url)
        return [
            OrgRoleRecord.parse_obj(record)
            for record in response.from_json(json_path=["data"])
        ]

    def get_org_by_id(self, org_id: str) -> OrgRecord:
        url = self.__http_client.url("v1/orgs")
        headers = {ORG_OVERRIDE_HEADER: org_id}
        response = self.__http_client.get(url=url, headers=headers)
        return OrgRecord.parse_obj(response.from_json(json_path=["data"]))

    def delete_org(self, org_id: str) -> None:
        url = self.__http_client.url("v1/orgs")
        headers = {ORG_OVERRIDE_HEADER: org_id}
        self.__http_client.delete(url=url, headers=headers)

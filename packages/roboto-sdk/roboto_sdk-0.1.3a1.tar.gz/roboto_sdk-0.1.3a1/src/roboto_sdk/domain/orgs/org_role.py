#  Copyright (c) 2023 Roboto Technologies, Inc.

from typing import Any

from ...serde import pydantic_jsonable_dict
from .delegate import OrgDelegate
from .org import Org
from .record import OrgRoleName, OrgRoleRecord


class OrgRole:
    __record: OrgRoleRecord
    __org_delegate: OrgDelegate
    __org: Org

    @classmethod
    def by_user_id(
        cls, user_id: str | None, org_delegate: OrgDelegate
    ) -> list["OrgRole"]:
        records = org_delegate.org_roles_for_user(user_id=user_id)
        return [cls(record=record, org_delegate=org_delegate) for record in records]

    def __init__(self, record: OrgRoleRecord, org_delegate: OrgDelegate):
        self.__record = record
        self.__org_delegate = org_delegate
        self.__org = Org(record=record.org, org_delegate=org_delegate)

    def to_dict(self) -> dict[str, Any]:
        return pydantic_jsonable_dict(self.__record)

    @property
    def org_id(self) -> str:
        return self.__record.org.org_id

    @property
    def org(self) -> Org:
        return self.__org

    @property
    def roles(self) -> list[OrgRoleName]:
        return self.__record.roles

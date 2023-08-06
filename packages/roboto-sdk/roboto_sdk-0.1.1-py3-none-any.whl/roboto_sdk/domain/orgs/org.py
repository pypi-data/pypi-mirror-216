#  Copyright (c) 2023 Roboto Technologies, Inc.

from typing import Any

from ...serde import pydantic_jsonable_dict
from .delegate import OrgDelegate
from .record import OrgRecord, OrgType


class Org:
    __record: OrgRecord
    __org_delegate: OrgDelegate

    @classmethod
    def create(
        cls,
        creator_user_id: str | None,
        name: str,
        org_type: OrgType,
        org_delegate: OrgDelegate,
    ):
        record = org_delegate.create_org(
            creator_user_id=creator_user_id, name=name, org_type=org_type
        )
        return cls(record=record, org_delegate=org_delegate)

    @classmethod
    def by_org_id(cls, org_id: str, org_delegate: OrgDelegate) -> "Org":
        record = org_delegate.get_org_by_id(org_id=org_id)
        return cls(record=record, org_delegate=org_delegate)

    @classmethod
    def by_user_id(cls, user_id: str | None, org_delegate: OrgDelegate) -> list["Org"]:
        records = org_delegate.orgs_for_user(user_id=user_id)
        return [cls(record=record, org_delegate=org_delegate) for record in records]

    def delete(self) -> None:
        self.__org_delegate.delete_org(org_id=self.org_id)

    def __init__(self, record: OrgRecord, org_delegate: OrgDelegate):
        self.__record = record
        self.__org_delegate = org_delegate

    def to_dict(self) -> dict[str, Any]:
        return pydantic_jsonable_dict(self.__record)

    @property
    def org_id(self):
        return self.__record.org_id

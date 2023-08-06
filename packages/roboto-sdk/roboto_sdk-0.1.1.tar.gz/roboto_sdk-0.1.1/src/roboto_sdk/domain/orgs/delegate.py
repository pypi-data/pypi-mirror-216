#  Copyright (c) 2023 Roboto Technologies, Inc.

import abc

from .record import (
    OrgRecord,
    OrgRoleRecord,
    OrgType,
)


class OrgDelegate(abc.ABC):
    @abc.abstractmethod
    def create_org(
        self, creator_user_id: str | None, name: str, org_type: OrgType
    ) -> OrgRecord:
        raise NotImplementedError("create_org")

    @abc.abstractmethod
    def orgs_for_user(self, user_id: str | None) -> list[OrgRecord]:
        raise NotImplementedError("orgs_for_user")

    @abc.abstractmethod
    def org_roles_for_user(self, user_id: str | None) -> list[OrgRoleRecord]:
        raise NotImplementedError("org_roles_for_user")

    @abc.abstractmethod
    def get_org_by_id(self, org_id: str) -> OrgRecord:
        raise NotImplementedError("get_org_by_id")

    @abc.abstractmethod
    def delete_org(self, org_id: str):
        raise NotImplementedError("delete_org")

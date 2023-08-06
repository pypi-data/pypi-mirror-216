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
        self,
        creator_user_id: str | None,
        name: str,
        org_type: OrgType,
        bind_email_domain: bool = False,
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

    @abc.abstractmethod
    def bind_email_domain(self, org_id: str, email_domain: str):
        raise NotImplementedError("bind_email_domain")

    @abc.abstractmethod
    def invite_user_to_org(
        self, invited_user_id: str, org_id: str, inviting_user_id: str | None = None
    ):
        raise NotImplementedError("invite_user_to_org")

    @abc.abstractmethod
    def accept_org_invite(self, invite_id: str, user_id: str | None = None):
        raise NotImplementedError("accept_org_invite")

    @abc.abstractmethod
    def decline_org_invite(self, invite_id: str, user_id: str | None = None):
        raise NotImplementedError("accept_org_invite")

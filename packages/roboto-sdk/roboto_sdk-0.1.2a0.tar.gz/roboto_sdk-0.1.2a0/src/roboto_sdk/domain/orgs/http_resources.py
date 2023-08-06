#  Copyright (c) 2023 Roboto Technologies, Inc.


import pydantic

from .record import OrgType


class CreateOrgRequest(pydantic.BaseModel):
    org_type: OrgType
    name: str
    bind_email_domain: bool = False


class BindEmailDomainRequest(pydantic.BaseModel):
    email_domain: str


class InviteUserRequest(pydantic.BaseModel):
    invited_user_id: str

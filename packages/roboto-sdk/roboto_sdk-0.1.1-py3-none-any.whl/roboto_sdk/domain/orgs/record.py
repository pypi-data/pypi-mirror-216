#  Copyright (c) 2023 Roboto Technologies, Inc.

import enum

import pydantic


class OrgType(str, enum.Enum):
    individual = "individual"
    team = "team"


class OrgTier(str, enum.Enum):
    free = "free"
    premium = "premium"


class OrgRecord(pydantic.BaseModel):
    org_id: str
    name: str
    org_type: OrgType
    tier: OrgTier
    members: int


class OrgRoleLevel(str, enum.Enum):
    user = "user"
    admin = "admin"


class OrgRoleRecord(pydantic.BaseModel):
    user_id: str
    org: OrgRecord
    roles: list[OrgRoleLevel]

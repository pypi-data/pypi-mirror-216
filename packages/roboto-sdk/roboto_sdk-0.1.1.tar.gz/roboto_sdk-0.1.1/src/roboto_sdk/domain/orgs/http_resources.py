#  Copyright (c) 2023 Roboto Technologies, Inc.


import pydantic

from .record import OrgType


class CreateOrgRequest(pydantic.BaseModel):
    org_type: OrgType
    name: str

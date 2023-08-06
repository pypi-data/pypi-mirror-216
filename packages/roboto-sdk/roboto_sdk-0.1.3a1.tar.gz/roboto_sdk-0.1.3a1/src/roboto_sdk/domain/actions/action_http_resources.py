from typing import Any

import pydantic

from .action_delegate import UpdateCondition


class CreateActionRequest(pydantic.BaseModel):
    # Required
    name: str

    # Optional
    description: str | None = None
    metadata: dict[str, Any] | None = pydantic.Field(default_factory=dict)
    tags: list[str] | None = pydantic.Field(default_factory=list)


class ContainerUploadCredentials(pydantic.BaseModel):
    username: str
    password: str
    registry_url: str
    image_uri: str


class UpdateActionRequest(pydantic.BaseModel):
    updates: dict[str, Any]
    conditions: list[UpdateCondition] | None = None
    tenant_id: str | None = None

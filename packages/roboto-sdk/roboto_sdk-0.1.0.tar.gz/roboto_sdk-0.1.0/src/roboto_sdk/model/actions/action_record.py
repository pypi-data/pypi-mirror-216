import datetime
from typing import Any

import pydantic


class ActionRecord(pydantic.BaseModel):
    """
    Actions are unique by their tenant_id and name.

    Note: update Action.DISALLOWED_FOR_UPDATE if necessary when adding/updating/removing fields.
    """

    created: datetime.datetime  # Persisted as ISO 8601 string in UTC
    created_by: str
    modified: datetime.datetime  # Persisted as ISO 8601 string in UTC
    modified_by: str
    name: str  # Sort key
    tenant_id: str  # Partition key

    description: str | None = None
    # Linked to `uri`; an Action may have a URI set but the container expected at that URI may not be available
    is_available: bool = False
    metadata: dict[str, Any] | None = None
    tags: list[str] | None = None
    uri: str | None = None

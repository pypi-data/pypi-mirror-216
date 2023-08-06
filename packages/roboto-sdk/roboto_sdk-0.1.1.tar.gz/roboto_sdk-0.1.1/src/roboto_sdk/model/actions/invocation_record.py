import datetime
import enum

import pydantic


class InvocationDataSourceType(enum.Enum):
    """Source of data for an Action's InputBinding"""

    Dataset = "Dataset"


class InvocationDataSource(pydantic.BaseModel):
    type: InvocationDataSourceType
    id: str | None = None


class InvocationSource(enum.Enum):
    Trigger = "Trigger"
    Manual = "Manual"


class InvocationDetail(pydantic.BaseModel):
    """Details why this Action was invoked."""

    type: InvocationSource
    # The “type” determines the meaning of “id:”
    #   - if type is “Trigger,” id is a TriggerId;
    #   - if type is “Manual,” id is a UserId.
    id: str


class InvocationStatus(enum.Enum):
    Queued = "Queued"
    Scheduled = "Scheduled"
    Downloading = "Downloading"
    Processing = "Processing"
    Uploading = "Uploading"
    Completed = "Completed"
    Failed = "Failed"
    Deadly = "Deadly"


class InvocationStatusRecord(pydantic.BaseModel):
    status: InvocationStatus
    detail: str | None = None
    timestamp: datetime.datetime  # Persisted as ISO 8601 string in UTC


class InvocationRecord(pydantic.BaseModel):
    id: str
    tenant_id: str
    action_name: str
    data_source: InvocationDataSource
    input_data: list[str]
    logs: str | None = None
    created: datetime.datetime  # Persisted as ISO 8601 string in UTC
    invoked_by: InvocationDetail
    status: list[InvocationStatusRecord] = pydantic.Field(default_factory=list)

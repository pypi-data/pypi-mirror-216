import pydantic

from ...model.actions import (
    InvocationDataSourceType,
    InvocationSource,
    InvocationStatus,
)


class CreateInvocationRequest(pydantic.BaseModel):
    input_data: list[str]
    data_source_id: str
    data_source_type: InvocationDataSourceType
    invocation_source: InvocationSource
    invocation_source_id: str | None


class UpdateInvocationStatus(pydantic.BaseModel):
    status: InvocationStatus
    detail: str

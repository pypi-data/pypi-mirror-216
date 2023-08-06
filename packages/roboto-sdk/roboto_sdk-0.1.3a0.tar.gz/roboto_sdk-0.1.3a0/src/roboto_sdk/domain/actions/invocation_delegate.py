import abc
from typing import Any

from ...pagination import PaginatedList
from .invocation_record import (
    InvocationDataSourceType,
    InvocationRecord,
    InvocationSource,
    InvocationStatus,
)


class InvocationDelegate(abc.ABC):
    @abc.abstractmethod
    def create_invocation(
        self,
        action_name: str,
        input_data: list[str],
        data_source_id: str,
        data_source_type: InvocationDataSourceType,
        invocation_source: InvocationSource,
        invocation_source_id: str | None = None,
        tenant_id: str | None = None,
    ) -> InvocationRecord:
        """Create an Invocation"""
        raise NotImplementedError("create_invocation")

    @abc.abstractmethod
    def get_by_id(
        self, invocation_id: str, org_id: str | None = None
    ) -> InvocationRecord:
        """Get an Invocation by ID"""
        raise NotImplementedError("get_by_id")

    @abc.abstractmethod
    def set_logs_location(
        self, record: InvocationRecord, bucket: str, prefix: str
    ) -> InvocationRecord:
        raise NotImplementedError("set_logs_location")

    @abc.abstractmethod
    def update_invocation_status(
        self,
        invocation: InvocationRecord,
        status: InvocationStatus,
        detail: str | None = None,
    ) -> InvocationRecord:
        """Update the status of an Invocation"""
        raise NotImplementedError("update_invocation_status")

    @abc.abstractmethod
    def query_invocations(
        self, filters: dict[str, Any], page_token: dict[str, str] | None = None
    ) -> PaginatedList[InvocationRecord]:
        raise NotImplementedError("query_actions")

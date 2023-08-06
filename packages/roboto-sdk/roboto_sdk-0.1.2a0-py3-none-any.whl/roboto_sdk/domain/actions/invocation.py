import collections.abc
from typing import Any

from ...serde import pydantic_jsonable_dict
from .invocation_delegate import (
    InvocationDelegate,
)
from .invocation_record import (
    InvocationDataSource,
    InvocationRecord,
    InvocationStatus,
)


class Invocation:
    __invocation_delegate: InvocationDelegate
    __record: InvocationRecord

    @classmethod
    def from_id(
        cls, invocation_id: str, invocation_delegate: InvocationDelegate
    ) -> "Invocation":
        record = invocation_delegate.get_by_id(invocation_id)
        return cls(record, invocation_delegate)

    @classmethod
    def query(
        cls, filters: dict[str, Any], invocation_delegate: InvocationDelegate
    ) -> collections.abc.Generator["Invocation", None, None]:
        known_keys = set(InvocationRecord.__fields__.keys())
        actual_keys = set(filters.keys())
        unknown_keys = actual_keys - known_keys
        if unknown_keys:
            plural = len(unknown_keys) > 1
            msg = (
                "are not known attributes of Invocation"
                if plural
                else "is not a known attribute of Invocation"
            )
            raise ValueError(f"{unknown_keys} {msg}. Known attributes: {known_keys}")

        paginated_results = invocation_delegate.query_invocations(filters)
        while True:
            for record in paginated_results.items:
                yield cls(record, invocation_delegate)
            if paginated_results.next_token:
                paginated_results = invocation_delegate.query_invocations(
                    filters, paginated_results.next_token
                )
            else:
                break

    def __init__(
        self, record: InvocationRecord, invocation_delegate: InvocationDelegate
    ) -> None:
        self.__invocation_delegate = invocation_delegate
        self.__record = record

    @property
    def action_name(self) -> str:
        return self.__record.action_name

    @property
    def data_source(self) -> InvocationDataSource:
        return self.__record.data_source

    @property
    def id(self) -> str:
        return self.__record.id

    @property
    def input_data(self) -> list[str]:
        return self.__record.input_data

    @property
    def logs_location(self) -> tuple[str, str] | None:
        if not self.__record.logs_bucket or not self.__record.logs_prefix:
            return None

        return self.__record.logs_bucket, self.__record.logs_prefix

    @property
    def org_id(self) -> str:
        return self.__record.tenant_id

    @property
    def status(self) -> InvocationStatus:
        status_record = self.__record.status[-1]
        return status_record.status

    def is_queued_for_scheduling(self) -> bool:
        """
        An invocation is queued for scheduling if it has not yet reached the "Scheduled" status
        and it is not "Deadly".
        """
        previously_scheduled_or_deadly = (
            InvocationStatus.Scheduled,
            InvocationStatus.Deadly,
        )
        return all(
            status_record.status not in previously_scheduled_or_deadly
            for status_record in self.__record.status
        )

    def set_logs_location(self, bucket: str, prefix: str) -> None:
        updated_record = self.__invocation_delegate.set_logs_location(
            self.__record, bucket, prefix
        )
        self.__record = updated_record

    def to_dict(self) -> dict[str, Any]:
        return pydantic_jsonable_dict(self.__record)

    def update_status(
        self, next_status: InvocationStatus, detail: str | None = "None"
    ) -> None:
        if next_status == InvocationStatus.Failed:
            # Heuristic: if this is the third time the invocation has failed, it is Deadly
            num_failures = len(
                [
                    status_record
                    for status_record in self.__record.status
                    if status_record.status == InvocationStatus.Failed
                ]
            )
            if num_failures >= 2:
                next_status = InvocationStatus.Deadly
        updated_record = self.__invocation_delegate.update_invocation_status(
            self.__record, next_status, detail
        )
        self.__record = updated_record

import collections.abc
from typing import Any

from ...serde import pydantic_jsonable_dict
from .invocation_delegate import (
    InvocationDelegate,
)
from .invocation_record import (
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

    def to_dict(self) -> dict[str, Any]:
        return pydantic_jsonable_dict(self.__record)

    def update_status(
        self, next_status: InvocationStatus, detail: str | None = "None"
    ) -> None:
        updated_record = self.__invocation_delegate.update_invocation_status(
            self.__record, next_status, detail
        )
        self.__record = updated_record

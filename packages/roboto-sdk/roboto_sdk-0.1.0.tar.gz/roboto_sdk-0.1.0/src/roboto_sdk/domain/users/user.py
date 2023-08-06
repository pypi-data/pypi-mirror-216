#  Copyright (c) 2023 Roboto Technologies, Inc.

from typing import Any

from ...serde import pydantic_jsonable_dict
from .user_delegate import UserDelegate
from .user_record import UserRecord


class User:
    __record: UserRecord
    __user_delegate: UserDelegate

    @classmethod
    def by_id(cls, user_id: str | None, user_delegate: UserDelegate):
        record = user_delegate.get_user_by_id(user_id=user_id)
        return cls(record=record, user_delegate=user_delegate)

    def __init__(self, record: UserRecord, user_delegate: UserDelegate):
        self.__record = record
        self.__user_delegate = user_delegate

    def to_dict(self) -> dict[str, Any]:
        return pydantic_jsonable_dict(self.__record)

    def delete(self) -> None:
        return self.__user_delegate.delete_user(user_id=self.__record.user_id)

    @property
    def user_id(self) -> str:
        return self.__record.user_id

    @property
    def username(self) -> str:
        return self.__record.user_id

    @property
    def is_system_user(self) -> bool:
        return (
            self.__record.is_system_user
            if self.__record.is_system_user is not None
            else False
        )

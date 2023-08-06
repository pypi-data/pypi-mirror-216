#  Copyright (c) 2023 Roboto Technologies, Inc.

import abc

from .user_record import UserRecord


class UserDelegate(abc.ABC):
    def __init__(self):
        super().__init__()

    @abc.abstractmethod
    def get_user_by_id(self, user_id: str | None) -> UserRecord:
        raise NotImplementedError("get_user_by_id")

    @abc.abstractmethod
    def delete_user(self, user_id: str | None) -> None:
        raise NotImplementedError("delete_user")

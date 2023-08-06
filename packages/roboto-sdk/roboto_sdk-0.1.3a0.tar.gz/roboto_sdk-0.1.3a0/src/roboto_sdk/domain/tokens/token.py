#  Copyright (c) 2023 Roboto Technologies, Inc.

from typing import Any

from ...serde import pydantic_jsonable_dict
from .delegate import TokenDelegate
from .record import TokenRecord


class Token:
    __record: TokenRecord
    __token_delegate: TokenDelegate

    @classmethod
    def by_token_id(cls, token_id: str, token_delegate: TokenDelegate) -> "Token":
        record = token_delegate.get_token_by_token_id(token_id=token_id)
        return cls(record=record, token_delegate=token_delegate)

    @classmethod
    def by_user_id(
        cls, user_id: str | None, token_delegate: TokenDelegate
    ) -> list["Token"]:
        records = token_delegate.get_tokens_for_user(user_id=user_id)
        return [cls(record=record, token_delegate=token_delegate) for record in records]

    @classmethod
    def create(
        cls,
        user_id: str | None,
        expiry_days: int,
        name: str,
        description: str | None,
        token_delegate: TokenDelegate,
    ):
        record = token_delegate.create_token(
            user_id=user_id, expiry_days=expiry_days, name=name, description=description
        )
        return cls(record=record, token_delegate=token_delegate)

    def delete(self):
        assert self.__record.context is not None
        return self.__token_delegate.delete_token(
            token_id=self.__record.context.token_id
        )

    def __init__(self, record: TokenRecord, token_delegate: TokenDelegate):
        self.__record = record
        self.__token_delegate = token_delegate

    def to_dict(self) -> dict[str, Any]:
        return pydantic_jsonable_dict(self.__record)

    @property
    def secret(self) -> str | None:
        return self.__record.secret

    @property
    def user_id(self) -> str | None:
        return self.__record.user_id

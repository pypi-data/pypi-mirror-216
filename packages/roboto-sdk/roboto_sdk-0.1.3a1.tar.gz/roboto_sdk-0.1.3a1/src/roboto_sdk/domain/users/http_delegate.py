#  Copyright (c) 2023 Roboto Technologies, Inc.

from ...http import (
    USER_OVERRIDE_HEADER,
    HttpClient,
)
from .user_delegate import UserDelegate
from .user_record import UserRecord


class UserHttpDelegate(UserDelegate):
    __http_client: HttpClient

    def __init__(self, http_client: HttpClient):
        super().__init__()
        self.__http_client = http_client

    def get_user_by_id(self, user_id: str | None) -> UserRecord:
        url = self.__http_client.url("v1/users")
        headers = {}
        if user_id is not None:
            headers[USER_OVERRIDE_HEADER] = user_id

        response = self.__http_client.get(url=url, headers=headers)
        return UserRecord.parse_obj(response.from_json(json_path=["data"]))

    def delete_user(self, user_id: str | None) -> None:
        url = self.__http_client.url("v1/users")
        headers = {}
        if user_id is not None:
            headers[USER_OVERRIDE_HEADER] = user_id

        self.__http_client.delete(url=url, headers=headers)

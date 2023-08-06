import abc
import datetime
from typing import Any, Literal

import pydantic

from ...pagination import PaginatedList
from ...serde import pydantic_jsonable_dict
from ...time import utcnow
from .action_record import ActionRecord


class ContainerCredentials(pydantic.BaseModel):
    username: str
    password: str
    registry_url: str
    expiration: datetime.datetime

    def is_expired(self) -> bool:
        return utcnow() >= self.expiration

    def to_dict(self) -> dict[str, Any]:
        return pydantic_jsonable_dict(self)


class UpdateCondition(pydantic.BaseModel):
    """
    A condition to be applied to an Action update operation.

    `value` is compared to the Action's current value of `key` using `comparator`.

    This is a severely constrainted subset of the conditions supported by DynamoDB. See:
    https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.OperatorsAndFunctions.html
    """

    key: str
    value: Any
    # Comparators are tied to convenience methods exposed on boto3.dynamodb.conditions.Attr. See:
    # https://github.com/boto/boto3/blob/5ad1a624111ed25efc81f425113fa51150516bb4/boto3/dynamodb/conditions.py#L246
    comparator: Literal["eq", "ne"]


class ActionDelegate(abc.ABC):
    @abc.abstractmethod
    def create_action(
        self,
        name: str,
        tenant_id: str | None = None,
        created_by: str | None = None,
        description: str | None = None,
        metadata: dict[str, Any] | None = None,
        tags: list[str] | None = None,
    ) -> ActionRecord:
        raise NotImplementedError("create_action")

    @abc.abstractmethod
    def get_action_by_primary_key(
        self, name: str, tenant_id: str | None = None
    ) -> ActionRecord:
        raise NotImplementedError("get_action_by_primary_key")

    @abc.abstractmethod
    def register_container(
        self,
        record: ActionRecord,
        image_name: str,
        image_tag: str,
        caller: str | None = None,
    ) -> tuple[str, str]:
        raise NotImplementedError("register_container")

    @abc.abstractmethod
    def get_temp_container_credentials(
        self,
        record: ActionRecord,
        caller: str | None = None,
    ) -> ContainerCredentials:
        raise NotImplementedError("get_temp_container_credentials")

    @abc.abstractmethod
    def query_actions(
        self, filters: dict[str, Any], page_token: dict[str, str] | None = None
    ) -> PaginatedList[ActionRecord]:
        raise NotImplementedError("query_actions")

    @abc.abstractmethod
    def update(
        self,
        record: ActionRecord,
        updates: dict[str, Any],
        conditions: list[UpdateCondition] | None,
        tenant_id: str | None = None,
    ) -> ActionRecord:
        raise NotImplementedError("update")

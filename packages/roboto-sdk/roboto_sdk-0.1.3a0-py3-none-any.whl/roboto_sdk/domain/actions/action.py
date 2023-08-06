import collections.abc
from typing import Any

from ...serde import pydantic_jsonable_dict
from .action_delegate import (
    ActionDelegate,
    ContainerCredentials,
    UpdateCondition,
)
from .action_record import ActionRecord
from .error import InvocationError
from .invocation import Invocation
from .invocation_delegate import (
    InvocationDelegate,
)
from .invocation_record import (
    InvocationDataSourceType,
    InvocationSource,
)


class Action:
    DISALLOWED_FOR_UPDATE = {"name", "tenant_id", "uri", "created_at", "created_by"}

    __action_delegate: ActionDelegate
    __invocation_delegate: InvocationDelegate
    __record: ActionRecord
    __temp_container_credentials: ContainerCredentials | None = None

    @classmethod
    def create(
        cls,
        name: str,
        action_delegate: ActionDelegate,
        invocation_delegate: InvocationDelegate,
        tenant_id: str | None = None,
        description: str | None = None,
        metadata: dict[str, Any] | None = None,
        tags: list[str] | None = None,
        created_by: str | None = None,
    ) -> "Action":
        record = action_delegate.create_action(
            name,
            tenant_id,
            created_by,
            description,
            metadata,
            tags,
        )
        return cls(record, action_delegate, invocation_delegate)

    @classmethod
    def by_name(
        cls,
        name: str,
        action_delegate: ActionDelegate,
        invocation_delegate: InvocationDelegate,
        tenant_id: str | None = None,
    ) -> "Action":
        record = action_delegate.get_action_by_primary_key(name, tenant_id)
        return cls(record, action_delegate, invocation_delegate)

    @classmethod
    def query(
        cls,
        filters: dict[str, Any],
        action_delegate: ActionDelegate,
        invocation_delegate: InvocationDelegate,
    ) -> collections.abc.Generator["Action", None, None]:
        known_keys = set(ActionRecord.__fields__.keys())
        actual_keys = set(filters.keys())
        unknown_keys = actual_keys - known_keys
        if unknown_keys:
            plural = len(unknown_keys) > 1
            msg = (
                "are not known attributes of Action"
                if plural
                else "is not a known attribute of Action"
            )
            raise ValueError(f"{unknown_keys} {msg}. Known attributes: {known_keys}")

        paginated_results = action_delegate.query_actions(filters)
        while True:
            for record in paginated_results.items:
                yield cls(record, action_delegate, invocation_delegate)
            if paginated_results.next_token:
                paginated_results = action_delegate.query_actions(
                    filters, paginated_results.next_token
                )
            else:
                break

    def __init__(
        self,
        record: ActionRecord,
        action_delegate: ActionDelegate,
        invocation_delegate: InvocationDelegate,
    ) -> None:
        self.__action_delegate = action_delegate
        self.__invocation_delegate = invocation_delegate
        self.__record = record

    @property
    def name(self) -> str:
        return self.__record.name

    @property
    def tenant_id(self) -> str:
        return self.__record.tenant_id

    @property
    def uri(self) -> str | None:
        return self.__record.uri

    def get_temporary_container_credentials(self) -> ContainerCredentials:
        if (
            self.__temp_container_credentials is None
            or self.__temp_container_credentials.is_expired()
        ):
            creds = self.__action_delegate.get_temp_container_credentials(self.__record)
            self.__temp_container_credentials = creds

        return self.__temp_container_credentials

    def invoke(
        self,
        input_data: list[str],
        data_source_id: str,
        data_source_type: InvocationDataSourceType,
        invocation_source: InvocationSource,
        invocation_source_id: str | None,
    ) -> Invocation:
        if self.__record.is_available is not True:
            raise InvocationError(
                "A container image must be associated with this Action and pushed before it can be invoked"
            )

        record = self.__invocation_delegate.create_invocation(
            self.__record.name,
            input_data,
            data_source_id,
            data_source_type,
            invocation_source,
            invocation_source_id,
            self.__record.tenant_id,
        )
        return Invocation(
            record,
            self.__invocation_delegate,
        )

    def register_container(
        self, image_name: str, image_tag: str, caller: str | None = None
    ) -> tuple[str, str]:
        """
        Idempotent get or create container repository for this Action, and associate it with the Action as its URI.
        Use this to associate an Action with a container image that has yet to be pushed,
        or with a container image that has already been pushed to an existing repository.

        A container may be pushed to the reposistory using credentials returned by
        `get_temporary_container_credentials`.
        Its tag does not need to equal `image_tag`, but without calling this method with the associated tag,
        the Action will not be able to invoke the pushed container.

        Side-effects:
            * If a container repository for given `image_name`:`image_tag` does not exist, it will be created.
            * If a container repository was previously created for this Action for a different `image_name`,
              AND that repository is empty, it will be deleted.
            * Sets the `uri` attribute of this Action to the URI of the image expected to be pushed to the repository.

        `caller` is ignored on the client. It is determined server-side via the identity/access mechanism.
        """
        return self.__action_delegate.register_container(
            self.__record, image_name, image_tag, caller
        )

    def to_dict(self) -> dict[str, Any]:
        return pydantic_jsonable_dict(self.__record)

    def update(
        self,
        updates: dict[str, Any],
        conditions: list[UpdateCondition] | None = None,
        tenant_id: str | None = None,
    ) -> None:
        known_keys = set(ActionRecord.__fields__.keys())
        allowed_keys = known_keys - Action.DISALLOWED_FOR_UPDATE
        unallowed = set(updates.keys()) - allowed_keys
        if len(unallowed):
            plural = len(unallowed) > 1
            msg = (
                "are not updateable attributes"
                if plural
                else "is not an updateable attribute"
            )
            raise ValueError(
                f"{unallowed} {msg}. Updateable attributes: {allowed_keys}"
            )

        updated = self.__action_delegate.update(
            self.__record, updates, conditions, tenant_id
        )
        self.__record = updated

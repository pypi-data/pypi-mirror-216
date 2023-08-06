import dataclasses
from typing import Generic, TypeVar

Model = TypeVar("Model")


@dataclasses.dataclass
class PaginatedList(Generic[Model]):
    items: list[Model]
    next_token: dict[str, str] | None = None

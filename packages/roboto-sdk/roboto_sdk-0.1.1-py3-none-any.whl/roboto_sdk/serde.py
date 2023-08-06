import json
import typing

import pydantic


def safe_dict_drill(
    target: dict[typing.Any, typing.Any], keys: list[typing.Any]
) -> typing.Any:
    value = target

    for key in keys:
        if type(value) is not dict:
            return None

        if key not in value:
            return None

        value = value[key]

    return value


def pydantic_jsonable_dict(model: pydantic.BaseModel, exclude_none=False) -> dict:
    return json.loads(model.json(exclude_none=exclude_none))


def pydantic_jsonable_dicts(models: list, exclude_none=False) -> list[dict]:
    return [pydantic_jsonable_dict(model, exclude_none) for model in models]

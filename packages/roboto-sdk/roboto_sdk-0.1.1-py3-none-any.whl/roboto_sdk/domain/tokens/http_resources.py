#  Copyright (c) 2023 Roboto Technologies, Inc.


import pydantic


class CreateTokenRequest(pydantic.BaseModel):
    expiry_days: int
    name: str
    description: str | None = None

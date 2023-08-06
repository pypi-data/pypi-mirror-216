#  Copyright (c) 2023 Roboto Technologies, Inc.


import datetime

import pydantic


class TokenContext(pydantic.BaseModel):
    token_id: str
    name: str
    description: str | None = None
    expires: datetime.datetime
    last_used: datetime.datetime | None = None


class TokenRecord(pydantic.BaseModel):
    secret: str | None = None
    user_id: str | None = None
    context: TokenContext | None = None

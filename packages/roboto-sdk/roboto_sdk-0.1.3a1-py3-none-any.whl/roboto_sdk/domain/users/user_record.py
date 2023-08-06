#  Copyright (c) 2023 Roboto Technologies, Inc.

import pydantic


class UserRecord(pydantic.BaseModel):
    user_id: str
    is_system_user: bool | None = False

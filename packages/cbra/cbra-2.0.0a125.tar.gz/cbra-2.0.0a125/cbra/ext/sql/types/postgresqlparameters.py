# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Literal

import pydantic


class PostgreSQLParameters(pydantic.BaseModel):
    engine: Literal['postgresql'] = pydantic.Field(
        alias='ENGINE'
    )

    host: str = pydantic.Field(
        alias='HOST'
    )

    port: int = pydantic.Field(
        alias='PORT'
    )

    name: str = pydantic.Field(
        alias='NAME'
    )

    user: str = pydantic.Field(
        alias='USER'
    )

    password: str = pydantic.Field(
        alias='PASSWORD'
    )

    @property
    def dsn(self) -> str:
        return f'postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}'
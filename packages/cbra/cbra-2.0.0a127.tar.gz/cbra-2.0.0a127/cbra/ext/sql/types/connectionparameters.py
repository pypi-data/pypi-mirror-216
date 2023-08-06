# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pydantic

from .postgresqlparameters import PostgreSQLParameters


class ConnectionParameters(pydantic.BaseModel):
    __root__: PostgreSQLParameters

    @property
    def dsn(self) -> str:
        return self.__root__.dsn
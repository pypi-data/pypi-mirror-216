# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import importlib
from typing import Any

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession

from .types import ConnectionParameters


class ConnectionRegistry:
    __module__: str = 'cbra.ext.sql'
    connections: dict[str, ConnectionParameters] = {}
    settings: Any = None

    def session(self, name: str, cls: type[AsyncSession] = AsyncSession) -> AsyncSession:
        factory: async_sessionmaker[cls] = async_sessionmaker(self.get(name), expire_on_commit=False)
        return factory()

    def get(self, name: str) -> AsyncEngine:
        """Return an :class:`sqlalchemy.ext.asyncio.AsyncEngine` instance."""
        if not self.settings:
            self.settings = importlib.import_module('cbra.core.conf').settings
            for connection_name, params in self.settings.DATABASES.items():
                self.connections[connection_name] = ConnectionParameters.parse_obj(params)
        return create_async_engine(self.connections[name].dsn)
    

connections: ConnectionRegistry = ConnectionRegistry()
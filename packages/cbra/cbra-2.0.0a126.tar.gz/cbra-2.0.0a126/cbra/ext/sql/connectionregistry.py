# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import importlib
import logging
from typing import Any

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession

from .types import ConnectionParameters


class ConnectionRegistry:
    __module__: str = 'cbra.ext.sql'
    connections: dict[str, ConnectionParameters] = {}
    logger: logging.Logger = logging.getLogger('cbra')
    settings: Any = None
    _engines: dict[str, AsyncEngine] = {}

    def __init__(self):
        self._engines = ConnectionRegistry._engines

    def dsn(self, name: str) -> str:
        return self.params(name).dsn

    async def dispose(self) -> None:
        """Close all engines."""
        self.logger.info("Disposing RDBMS connections")
        for name, engine in self._engines.items():
            self.logger.debug("Disposing %s", name)
            await engine.dispose()

    def session(self, name: str, cls: type[AsyncSession] = AsyncSession) -> AsyncSession:
        factory: async_sessionmaker[cls] = async_sessionmaker(self.get(name), expire_on_commit=False)
        return factory()

    def params(self, name: str) -> ConnectionParameters:
        if not self.settings:
            self.settings = importlib.import_module('cbra.core.conf').settings
            for connection_name, params in self.settings.DATABASES.items():
                self.connections[connection_name] = ConnectionParameters.parse_obj(params)
        return self.connections[name]       

    def get(self, name: str) -> AsyncEngine:
        """Return an :class:`sqlalchemy.ext.asyncio.AsyncEngine` instance."""
        params = self.params(name)
        if name not in self._engines:
            self._engines[name] = create_async_engine(params.dsn)
        return self._engines[name]
    

connections: ConnectionRegistry = ConnectionRegistry()

del ConnectionRegistry
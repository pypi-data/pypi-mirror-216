# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import fastapi
import sqlalchemy.ext.asyncio

from .connectionregistry import connections


class Session(sqlalchemy.ext.asyncio.AsyncSession):
    __module__: str = 'cbra.ext.sql'

    @classmethod
    def inject(cls, name: str = 'default'):
        async def f():
            session = connections.session(name, cls=cls)
            try:
                yield session
            finally:
                await session.close()

        return fastapi.Depends(f)
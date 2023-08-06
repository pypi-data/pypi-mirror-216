# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio
import functools
import logging
from typing import Any
from typing import Awaitable
from typing import Callable
from typing import ParamSpec
from typing import TypeVar

import fastapi
import sqlalchemy.exc
import sqlalchemy.ext.asyncio

from .connectionregistry import connections


_P = ParamSpec('_P')
_T = TypeVar("_T", bound=Any)
logger: logging.Logger = logging.getLogger('cbra')


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
    
    @staticmethod
    def retry(
        max_attempts: int,
        delay: float = 0.0,
        catch: tuple[type[BaseException], ...] = (
            sqlalchemy.exc.TimeoutError,
        ),
    ) -> Callable[
        [Callable[_P, Awaitable[_T]]],
        Callable[_P, Awaitable[_T]]
    ]:

        def decorator_factory(func: Callable[_P, Awaitable[_T]]) -> Callable[_P, Awaitable[_T]]:
            @functools.wraps(func)
            async def f(*args: Any, **kwargs: Any) -> _T:
                _attempts = kwargs.pop('_attempts', 1)
                try:
                    return await func(*args, **kwargs) # type: ignore
                except catch:
                    if _attempts > max_attempts:
                        raise
                    if delay:
                        await asyncio.sleep(delay)
                    return await f(_attempts=_attempts + 1, *args, **kwargs)
            return f # type: ignore

        return decorator_factory
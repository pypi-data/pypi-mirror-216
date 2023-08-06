# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import cast

import fastapi

from ..connectionregistry import connections
from ..const import DEFAULT_CONNECTION_NAME
from ..session import Session


__all__: list[str] = ['DefaultSession']


async def get() -> Session:
    return cast(Session, connections.session(DEFAULT_CONNECTION_NAME))


DefaultSession: Session = fastapi.Depends(get)
# Copyright (C) 2020-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import inspect
#from collections import OrderedDict
from typing import Any
from typing import Awaitable
from typing import Callable
from typing import TypeVar

import fastapi
from fastapi.concurrency import AsyncExitStack
from fastapi.params import Depends
from fastapi.dependencies.utils import get_dependant
from fastapi.dependencies.utils import solve_dependencies

#from cbra.types import IDependant
from .container import Container
from .requirement import Requirement


R = TypeVar('R')

_injectables: tuple[type, ...] = (
    Depends,
    Requirement
)

def update_requirements(container: Container, func: Callable[..., Any] | Depends | Any) -> None:
    """Traverse the signature tree of the given function to find
    all :class:`Requirement` instances.
    """
    # TODO: this will completely mess up if multiple Application instances
    # are spawned.
    if not callable(func): return None
    if isinstance(func, Requirement):
        func.add_to_container(container)
    elif isinstance(func, Depends):
        return update_requirements(container, func.dependency)
    try:
        signature = inspect.signature(func) # type: ignore
    except ValueError:
        # No signature to inspect.
        return None
    
    #replaced: list[inspect.Parameter] = []
    for param in signature.parameters.values():
        if isinstance(param.default, Requirement):
            param.default.add_to_container(container)
            if param.default.callable():
                update_requirements(container, param.default.factory)
            continue
        if isinstance(param.default, Depends): # type: ignore
            injectable = param.default.dependency
            if injectable is None:
                # Was declared as f(dependency: Callable = fastapi.Depends())
                injectable = param.annotation
            update_requirements(container, injectable)
        #if inspect.isclass(param.annotation)\
        #and issubclass(param.annotation, IDependant)\
        #and param.default != inspect.Parameter.empty:
        #    replaced.append(param.replace(default=fastapi.Depends(param.annotation.__inject__())))
        #    update_requirements(container, replaced[-1])

    #parameters: OrderedDict[str, inspect.Parameter] = OrderedDict(signature.parameters)
    #for param in replaced:
    #    parameters[param.name] = param
    #func.__signature__ = signature.replace(parameters=parameters.values()) # type: ignore



async def run(
    f: Callable[..., Awaitable[R] | R],
    *,
    container: Container | None = None,
    scope: dict[str, Any] | None = None,
    **kwargs: Any
) -> R:
    container = container or Container.fromsettings()
    async with AsyncExitStack() as stack:
        request: fastapi.Request = fastapi.Request({
            **(scope or {}),
            'fastapi_astack': stack,
            'headers': [],
            'query_string': None,
            'type': 'http',
        })

        update_requirements(container, f)
        dependant = get_dependant(call=f, path='/')
        values, errors, *_ = await solve_dependencies(
            request=request,
            dependant=dependant,
            body=None,
            dependency_overrides_provider=None
        )
        kwargs = {
            **values,
            **kwargs
        }
        if errors:
            raise Exception(errors)
        assert callable(dependant.call)
        result = dependant.call(**kwargs)
        if inspect.isawaitable(result):
            result = await result
        return result
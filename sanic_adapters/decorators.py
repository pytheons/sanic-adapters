from functools import reduce
from typing import Type

from sanic_adapters.formatters import Formatters
from sanic_adapters.models import URLSpaceFormat
from sanic_adapters.resources import (
    RESTResource,
)
from sanic_adapters.routing import (
    RoutePart,
    Routing,
    Route
)

class ResourceOverride:
    def __init__(self, path: str):
        self.path = path

    def __call__(self, cls: Type[RESTResource]):
        name = Formatters.to_underscore(cls.__name__)
        Routing.route_parts[cls.__name__] = RoutePart(url_prefix=self.path, name=str(name))
        return cls

def route(name: str, path: str, http_method: str = None):
    def route_decorator(handler):
        new_route = Route(name, path, http_method, handler)
        Routing.register(new_route)
        return new_route()
    return route_decorator
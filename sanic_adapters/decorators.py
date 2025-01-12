from typing import Type

from sanic_adapters.formatters import Formatters
from sanic_adapters.resources import RESTResource
from sanic_adapters.routing import (
    Route,
    RoutePart,
    Routing,
)


class ResourceOverride:
    def __init__(self, path: str):
        self.path = path

    def __call__(self, cls: Type[RESTResource]):
        name = Formatters.to_underscore(cls.__name__)
        if not Routing.route_parts[cls.__name__]:
            Routing.route_parts[cls.__name__] = RoutePart(url_prefix=self.path, name=name)
            return cls

        Routing.route_parts[cls.__name__].url_prefix = self.path
        return cls

def route(name: str, path: str, http_method: str = None) -> callable:
    def route_decorator(handler):
        new_route = Route(name, path, http_method, handler)
        Routing.register(new_route)
        return handler
    return route_decorator
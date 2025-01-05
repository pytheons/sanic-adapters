import inspect
from typing import (
    Dict,
    List,
)

from sanic.models.futures import FutureRoute
from sanic_routing import Route as SanicRoute

from sanic_adapters.formatters import Formatters
from sanic_adapters.resources import RESTResource, Route, RoutePart


class Routing:
    __routes: List[FutureRoute | SanicRoute] = []
    route_parts: Dict[str, RoutePart] = {}

    @classmethod
    def register(cls, route: Route) -> None:
        class_name = Formatters.get_class_name(route)
        route_part_name = Formatters.to_underscore(class_name)

        url_path = Formatters.to_url_format(route_part_name)
        route_part = RoutePart(url_prefix=url_path, name=str(route_part_name))


        if class_name not in cls.route_parts:
            cls.route_parts[class_name] = route_part

        cls.__add_route(class_name, route)

    @classmethod
    def __add_route(cls, class_name: str, route: Route) -> None:
        args = inspect.signature(route.function)
        http_method = route.get_http_method()

        if "self" not in args.parameters:
            cls.route_parts[class_name].add_route(route.function, route.path, name=route.name, methods=[http_method])
            return

        resource_name = f"{class_name}{str(route.name).title().replace("_", "")}"
        resource: RESTResource | type = type(resource_name, (RESTResource,), {http_method.lower(): route.function})
        cls.route_parts[class_name].add_route(resource.as_view(), route.path, name=route.name, methods=[http_method])
        route_part = cls.route_parts[class_name]
        if cls.__routes and getattr(route_part, '_future_routes') not in cls.__routes:
            cls.__routes.extend(getattr(route_part, '_future_routes'))


    @classmethod
    def routes(cls):
        for route_part in cls.route_parts.values():
            if route_part.routes:
                cls.__routes.extend(route_part.routes)
            if getattr(route_part, "_future_routes"):
                cls.__routes.extend(getattr(route_part, "_future_routes"))

        return cls.__routes

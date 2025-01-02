from dataclasses import dataclass, field
from functools import reduce
from typing import Dict, List

from sanic import Blueprint
from sanic.constants import HTTP_METHODS


@dataclass
class Route:
    name: str
    path: str
    method: str = field(default=None)
    function: callable = field(default=None)
    class_name: str = field(default=None)

    def __call__(self):
        self.function.name = self.name
        self.function.path = self.path
        self.function.method = self.method
        self.function.class_name = self.class_name

        return self.function

    def __post_init__(self):
        try:
            assert self.name, "Name is required"
            assert isinstance(self.name, str), "Name must be a valid string"

            assert self.path, "Path is required"
            assert isinstance(self.path, str), "Path must be a valid string"

            assert self.method is None or (
                self.method and isinstance(self.method, str)
                and self.method in HTTP_METHODS
            ), "Method must be a valid string and valid HTTP method"
        except AssertionError as exception:
            raise ValueError(exception)


class RoutePart(Blueprint): ...


class Routing:
    routes: List[Route] = []
    route_parts: Dict[str, RoutePart] = {}

    @classmethod
    def register(cls, route: Route) -> None:
        class_name = str(route.function.__qualname__).replace(f".{route.function.__name__}", "")
        name = reduce(lambda x, y: x + ("_" if y.isupper() else "") + y, class_name).lower()
        url_path = f"{str(name).replace("_", "-")}"
        resource = RoutePart(url_prefix=url_path, name=str(name))
        if class_name not in cls.route_parts:
            cls.route_parts[class_name] = resource

        Routing.routes.append(route)

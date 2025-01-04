import logging
from dataclasses import dataclass, field
from functools import reduce
from typing import (
    Callable,
    Dict,
    List,
)

from sanic import Blueprint
from sanic.base.root import VALID_NAME
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


class Formatters:
    @classmethod
    def get_qual_name(cls, function: Callable) -> str:
        qual_names = str(function.__qualname__).split(".")
        qual_name = qual_names[-1]
        if qual_names and len(qual_names) >= 2:
            qual_name = qual_names[-2]
        return qual_name

    @classmethod
    def get_class_name(cls, route: Route):
        qual_name = cls.get_qual_name(route.function)
        class_name = qual_name.replace(f".{route.function.__name__}", "")
        if not VALID_NAME.match(class_name):
            class_name = route.class_name
        return class_name

    @classmethod
    def to_underscore(cls, camel_case: str) -> str:
        return reduce(lambda x, y: x + ("_" if y.isupper() else "") + y, camel_case).lower()

    @classmethod
    def to_url_format(cls, some_string: str) -> str:
        return f"{str(some_string).replace("_", "-")}"

class Routing:
    routes: List[Route] = []
    route_parts: Dict[str, RoutePart] = {}

    @classmethod
    def register(cls, route: Route) -> None:
        class_name = Formatters.get_class_name(route)
        name = Formatters.to_underscore(class_name)
        url_path = Formatters.to_url_format(route.path)
        resource = RoutePart(url_prefix=url_path, name=str(name))
        if class_name not in cls.route_parts:
            cls.route_parts[class_name] = resource

        cls.routes.append(route)

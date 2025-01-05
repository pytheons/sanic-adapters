from dataclasses import (
    dataclass,
    field,
)
from typing import Callable

from sanic import Blueprint
from sanic.constants import HTTP_METHODS
from sanic.views import HTTPMethodView


@dataclass
class Route:
    name: str
    path: str
    method: str = field(default=None)
    function: callable = field(default=None)
    class_name: str = field(default=None)

    def get_http_method(self) -> str:
        return self.method or self.function.__name__.split("_")[0].upper()

    def __post_init__(self):
        try:
            assert self.name, "Name is required"
            assert isinstance(self.name, str), "Name must be a valid string"

            assert self.path, "Path is required"
            assert isinstance(self.path, str), "Path must be a valid string"

            assert self.method is None or (
                isinstance(self.method, str)
                and self.method in HTTP_METHODS
            ), "Method must be a valid string and valid HTTP method"

            assert self.function is None or isinstance(self.function, Callable), "Function must be a valid callable"
            assert self.class_name is None or isinstance(self.class_name, str), "Class name must be a valid string"
        except AssertionError as exception:
            raise ValueError(exception)

class RoutePart(Blueprint): ...

class RESTResource(HTTPMethodView): ...

from dataclasses import (
    dataclass,
    field,
)
from enum import Enum

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

class RESTResource(HTTPMethodView): ...

class URLSpaceFormat(Enum):
    KEBAB = "-"
    UNDERSCORE = "_"

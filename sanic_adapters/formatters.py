from functools import reduce
from typing import Callable

from sanic.base.root import VALID_NAME

from sanic_adapters.resources import Route


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

import re
from typing import Callable

from hypothesis import given
from pytest import mark, raises
from hypothesis.strategies import (
    booleans,
    floats,
    from_regex,
    integers,
    lists,
    one_of,
    sets,
    text,
    tuples,
)
from sanic.constants import HTTP_METHODS

from sanic_adapters.resources import Route


class TestRoute:
    @given(
        name=one_of(
            integers(),
            text(max_size=0),
            booleans(),
            floats(),
            lists(one_of(integers(), booleans(), floats(), text())),
            sets(
                one_of(
                    integers(),
                    booleans(),
                    floats(),
                    text(),
                ),
            ),
            tuples(
                one_of(
                    integers(),
                    booleans(),
                    floats(),
                    text(),
                ),
            ),
        ),
    )
    def test_name_passed_with_wrong_type_to_route_when_is_string_than_route_raises_value_error(self, name: str | int):
        with raises(ValueError):
            Route(name=name, path="/test")

    @given(name=text(min_size=1))
    def test_name_passed_correct_type_to_route_when_is_string_than_route_returns_string(self, name: str | int):
        route = Route(name=name, path="/test")

        assert route.name == name and isinstance(route.name, str), "Name must be string"

    @given(
        path=one_of(
            integers(),
            text(max_size=0),
            booleans(),
            floats(),
            lists(one_of(integers(), booleans(), floats(), text())),
            sets(
                one_of(
                    integers(),
                    booleans(),
                    floats(),
                    text(),
                ),
            ),
            tuples(
                one_of(
                    integers(),
                    booleans(),
                    floats(),
                    text(),
                ),
            ),
        ),
    )
    def test_path_passed_with_wrong_type_to_route_when_is_string_than_route_raises_value_error(self, path: str | int):
        with raises(ValueError):
            Route(name="x", path=path)

    @given(path=from_regex(r"^/[A-Za-z0-9/]+", fullmatch=True))
    def test_path_passed_correct_type_to_route_when_is_string_than_route_returns_string(self, path: str | int):
        route = Route(name="x", path=path)

        assert (
            route.path == path and isinstance(route.path, str) and re.match("/[A-Za-z0-9]*", route.path)
        ), "Path must be valid string"

    def test_when_only_required_fields_are_passed_then_method_field_are_not_set_by_default(self):
        route = Route(name="x", path="/test")
        assert route.method is None, "Method is set by default"

    @given(
        method=one_of(
            integers(),
            text(),
            booleans(),
            floats(),
            lists(one_of(integers(), booleans(), floats(), text())),
            sets(
                one_of(
                    integers(),
                    booleans(),
                    floats(),
                    text(),
                ),
            ),
            tuples(
                one_of(
                    integers(),
                    booleans(),
                    floats(),
                    text(),
                ),
            ),
        ),
    )
    def test_when_incorrect_method_passed_then_route_raises_exception(self, method: str):
        with raises(ValueError):
            Route(name="x", path="/test", method=method)

    @mark.parametrize("method", HTTP_METHODS)
    def test_when_correct_method_passed_then_route_accept(self, method: str):
        Route(name="x", path="/test", method=method)

    def test_route_create_when_function_not_passed_then_route_function_is_none(self):
        route = Route(name="x", path="/test", method="GET")
        assert not route.function, f"Function expected as None, but got '{type(route.function)}'"

    def test_when_correct_function_passed_then_route_function_is_callable(self):
        route = Route(name="x", path="/test", method="GET", function=lambda x: x)
        assert isinstance(route.function, Callable), f"Function expected as callable, but got '{type(route.function)}'"

    def test_route_create_when_class_name_not_passed_then_route_class_name_is_none(self):
        route = Route(name="x", path="/test", method="GET")
        assert not route.class_name, f"Function expected as None, but got '{type(route.class_name)}'"

    def test_when_correct_class_name_passed_then_route_class_name_is_set(self):
        route = Route(name="x", path="/test", method="GET", function=lambda x: x, class_name="string")
        message = f"Class name expected as correct string, but got '{type(route.class_name)}'"
        assert route.class_name and isinstance(route.class_name, str), message


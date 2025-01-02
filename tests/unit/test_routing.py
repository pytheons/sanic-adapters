from hypothesis import given
from hypothesis.strategies import (booleans, floats, from_regex, integers,
                                   lists, one_of, sets, text, tuples)
from pytest import mark, raises
from sanic.constants import HTTP_METHODS

from sanic_adapters.routing import Route


class TestRoute:
    @mark.parametrize(
        "name",
        [
            integers().example(),
            text(max_size=0).example(),
            booleans().example(),
            floats().example(),
            lists(one_of(integers(), booleans(), floats(), text())).example(),
            sets(
                one_of(
                    integers(),
                    booleans(),
                    floats(),
                    text(),
                ),
            ).example(),
            tuples(
                one_of(
                    integers(),
                    booleans(),
                    floats(),
                    text(),
                ),
            ).example(),
        ],
    )
    def test_name_passed_with_wrong_type_to_route_when_is_string_than_route_raises_value_error(self, name: str | int):
        with raises(ValueError):
            Route(name=name, path="/test")

    @mark.parametrize("name", [text(min_size=1).example()])
    def test_name_passed_correct_type_to_route_when_is_string_than_route_returns_string(self, name: str | int):
        route = Route(name=name, path="/test")

        assert route.name == name and isinstance(route.name, str), "Name must be string"

    @mark.parametrize(
        "path",
        [
            integers().example(),
            text(max_size=0).example(),
            booleans().example(),
            floats().example(),
            lists(one_of(integers(), booleans(), floats(), text())).example(),
            sets(
                one_of(
                    integers(),
                    booleans(),
                    floats(),
                    text(),
                ),
            ).example(),
            tuples(
                one_of(
                    integers(),
                    booleans(),
                    floats(),
                    text(),
                ),
            ).example(),
        ],
    )
    def test_path_passed_with_wrong_type_to_route_when_is_string_than_route_raises_value_error(self, path: str | int):
        with raises(ValueError):
            Route(name="x", path=path)

    @given(path=from_regex("/[A-Za-z0-9].*"))
    def test_path_passed_correct_type_to_route_when_is_string_than_route_returns_string(self, path: str | int):
        route = Route(name="x", path=path)

        assert route.path == path and isinstance(route.path, str), "Path must be string"

    def test_when_only_required_fields_are_passed_then_method_field_are_not_set_by_default(self):
        route = Route(name="x", path="/test")
        assert route.method is None, "Method is set by default"

    @mark.parametrize(
        "method",
        [
            integers().example(),
            text().example(),
            booleans().example(),
            floats().example(),
            lists(one_of(integers(), booleans(), floats(), text())).example(),
            sets(
                one_of(
                    integers(),
                    booleans(),
                    floats(),
                    text(),
                ),
            ).example(),
            tuples(
                one_of(
                    integers(),
                    booleans(),
                    floats(),
                    text(),
                ),
            ).example(),
        ],
    )
    def test_when_incorrect_method_passed_then_route_raises_exception(self, method: str):
        with raises(ValueError):
            Route(name="x", path="/test", method=method)

    @mark.parametrize("method", HTTP_METHODS)
    def test_when_correct_method_passed_then_route_accept(self, method: str):
        Route(name="x", path="/test", method=method)

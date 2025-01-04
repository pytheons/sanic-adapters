import re

from examples import (Examples, nested_3_layers_function, top_level_function,
                      top_level_function_with_nested_function)
from hypothesis import given
from hypothesis.strategies import (booleans, floats, from_regex, functions,
                                   integers, lists, one_of, sets, text, tuples)
from pytest import mark, raises
from sanic.constants import HTTP_METHODS
from typing_extensions import Callable

from sanic_adapters.routing import Route, Routing


class TestRouting:
    @given(
        one_of(
            functions(like=lambda x: x),
            functions(like=top_level_function),
            functions(
                like=top_level_function_with_nested_function(),
            ),
            functions(
                like=nested_3_layers_function(),
            ),
            functions(like=Examples.class_method),
            functions(
                like=Examples().class_method_with_nested_function(),
            ),
            functions(
                like=Examples().class_method_with_nested_class(),
            ),
            functions(like=Examples().class_method_with_nested_class_with_nested_function()),
        )
    )
    def test_given_route_when_register_by_routing_then_resource_and_route_will_be_added(self, function: Callable):
        route = Route(name="test", path="/test", method="GET", function=function, class_name="MyResource")
        Routing.register(route)

        assert route in Routing.routes, "Expected route to be registered, but route not found in Routing.routes"
        assert Routing.route_parts, f"Expected route parts to be registered, but got {Routing.route_parts=}"

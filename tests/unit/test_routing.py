from hypothesis import given
from hypothesis.strategies import (
    functions,
    one_of,
)
from typing_extensions import Callable

from examples.functions import (
    Examples,
    nested_3_layers_function,
    top_level_function,
    top_level_function_with_nested_function,
)
from sanic_adapters.resources import RoutePart
from sanic_adapters.routing import (
    Route,
    Routing,
)


class TestRouting:
    @given(
        one_of(
            functions(like=lambda request: request.route),
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

        assert Routing.route_parts, f"Expected route parts to be registered, but got {Routing.route_parts=}"

    def test_routing_routes_work_as_same_as_future_routes(self):
        routes = set()
        for route_part in Routing.route_parts.values():
            for route in getattr(route_part,"_future_routes"):
                routes.add(route)
            route_part.routes.extend(list(routes))
            route_part._future_routes = set()
            break

        assert routes.issubset(set(Routing.routes())), f"Expected routes to be registered, but got {routes=}"


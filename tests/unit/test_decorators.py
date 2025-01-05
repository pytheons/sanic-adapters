from pytest import fixture

from sanic_adapters.decorators import (
    ResourceOverride,
    route,
)
from sanic_adapters.resources import RESTResource
from sanic_adapters.routing import Routing


class TestResourceOverride:
    def test_resource_override_decorator_when_class_is_wrapped_then_register_route_has_correct_values(self, resource_override):
        print()
        for my_route in Routing.routes():
            if my_route.name == "my_route.my_route":
                assert my_route.uri == "/inside", "Expected 'my_route.my_route.my_route' to be 'my_route.my_route'"

    @fixture
    def resource_override(self):
        @ResourceOverride(path="/prefix")
        class MyRoute(RESTResource):
            @route(name="my_route", path="/inside")
            async def get(self, request):
                return {"my-route": f"{request=}"}

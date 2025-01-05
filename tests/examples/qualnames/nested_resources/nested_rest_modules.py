from sanic_adapters.decorators import route
from sanic_adapters.resources import RESTResource


class NestedTestController(RESTResource):
    @staticmethod
    @route(name="nested_test_route", path="/")
    async def get(request):

        return {'hello': 'world', "request": request.get_json()}
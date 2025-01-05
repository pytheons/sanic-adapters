from sanic_adapters.resources import RESTResource
from sanic_adapters.decorators import route


class TestController(RESTResource):
    @route(name="test_name", path="/")
    async def get(self, request):
        return {"test": f"{self.__class__.__name__}"}

    @classmethod
    @route(name="test_name_static", path="/test")
    async def get_static(cls, request):
        return {"static": f"{request=}"}
from typing import (
    Dict,
    List,
)

from sanic_adapters.formatters import Formatters
from sanic_adapters.models import (
    Route,
    RoutePart,
)


class Routing:
    routes: List[Route] = []
    route_parts: Dict[str, RoutePart] = {}

    @classmethod
    def register(cls, route: Route) -> None:
        class_name = Formatters.get_class_name(route)
        name = Formatters.to_underscore(class_name)
        url_path = Formatters.to_url_format(route.path)
        resource = RoutePart(url_prefix=url_path, name=str(name))
        if class_name not in cls.route_parts:
            cls.route_parts[class_name] = resource

        cls.routes.append(route)

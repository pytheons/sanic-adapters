import importlib
import inspect
import os
from importlib import (
    import_module,
    util,
)
from importlib.metadata import PackageNotFoundError
from pathlib import Path
from typing import (
    List,
)

from sanic_adapters.models import (
    RESTResource,
    RoutePart,
)
from sanic_adapters.routing import (
    Routing,
)
from sanic.views import HTTPMethodView

class RESTFramework:
    @classmethod
    def autodiscover(cls, package: str) -> List[RoutePart]:
        for module in cls.__list_modules__(package):
            import_module(module)

        for route in Routing.routes:
            methods = [route.method or route.function.__name__.split("_")[0].upper()]
            class_name = str(route.function.__qualname__).replace(f".{route.function.__name__}", "")
            type_name = f"{class_name}{str(route.name).title().replace("_", "")}"
            resource: RESTResource | type = type(type_name, (RESTResource,), {str(methods[0]).lower(): route.function})
            args = inspect.signature(route.function)

            if 'self' not in args.parameters:
                Routing.route_parts[class_name].add_route(route.function, route.path, name=route.name, methods=methods)
                continue

            Routing.route_parts[class_name].add_route(resource.as_view(), route.path, name=route.name, methods=methods)
        return list(Routing.route_parts.values())

    @classmethod
    def __list_modules__(cls, package_name: str):
        spec = importlib.util.find_spec(package_name)
        if spec is None:
            raise PackageNotFoundError(package_name)
        pathname = Path(spec.origin).parent
        modules = set()
        with os.scandir(pathname) as entries:
            for entry in entries:
                if entry.name.startswith('__'):
                    continue
                current = '.'.join((package_name, entry.name.partition('.')[0]))
                if entry.is_file():
                    if entry.name.endswith(".py"):
                        modules.add(current)
                elif entry.is_dir():
                    modules.add(current)
                    modules |= cls.__list_modules__(current)

        return modules

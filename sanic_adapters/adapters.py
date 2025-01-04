import os
from importlib import import_module
from importlib.metadata import PackageNotFoundError
from importlib.util import find_spec
from pathlib import Path
from typing import List

from sanic_adapters.resources import RoutePart
from sanic_adapters.routing import Routing


class RESTFramework:
    @classmethod
    def autodiscover(cls, package: str) -> List[RoutePart]:
        for module in cls.__list_modules__(package):
            import_module(module)

        return list(Routing.route_parts.values())

    @classmethod
    def __list_modules__(cls, package_name: str):
        spec = find_spec(package_name)
        if spec is None:
            raise PackageNotFoundError(package_name)
        pathname = Path(spec.origin).parent
        modules = set()
        with os.scandir(pathname) as entries:
            for entry in entries:
                if entry.name.startswith("__"):
                    continue
                current = ".".join((package_name, entry.name.partition(".")[0]))
                if entry.is_file():
                    if entry.name.endswith(".py"):
                        modules.add(current)
                elif entry.is_dir():
                    modules.add(current)
                    modules |= cls.__list_modules__(current)

        return modules

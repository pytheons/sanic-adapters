import os
from importlib import import_module
from importlib.metadata import PackageNotFoundError
from importlib.util import find_spec
from pathlib import Path
from typing import (
    List,
    Tuple,
)

from dependency_injector import providers
from dependency_injector.containers import DynamicContainer
from dependency_injector.providers import Configuration
from dependency_injector.wiring import provided
from sanic import Sanic

from sanic_adapters.resources import RoutePart
from sanic_adapters.routing import Routing


class RESTFramework:
    sanic: Sanic

    def __init__(self, sanic: Sanic, package: str):
        self.sanic = sanic
        self.sanic.blueprint(self.autodiscover(package))

    @classmethod
    def autodiscover(cls, package: str) -> List[RoutePart]:
        for module in cls.__list_modules__(package):
            import_module(module)

        return list(Routing.route_parts.values())

    @classmethod
    def __list_modules__(cls, package_name: str):
        try:
            spec = find_spec(package_name)
        except ModuleNotFoundError:
            spec = None

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

class Container(DynamicContainer):
    config: Configuration = Configuration()

class IoC:
    services: Container = None

    def __init__(self, sanic: Sanic, config: str):
        if not self.__class__.services:
            self.__class__.services = Container()
            self.services.config.from_yaml(config)
            sanic.ext.dependency(self)

            for service_name, service_definition in self.services.config().items():
                module_path, class_name = self.__parse_service_path__(service_definition.get("class"))
                module = import_module(module_path)
                service_class = getattr(module, class_name)
                provided_by = getattr(providers, service_definition["provided_by"])
                setattr(self.services, service_name, provided_by(service_class))
                sanic.ext.add_dependency(service_class)

    @staticmethod
    def __parse_service_path__(service_path: str = None) -> Tuple[str, str]:
        service_path_parts = service_path.split(".")

        return ".".join(service_path_parts[:-1]), service_path_parts[-1]


from pytest import raises
from importlib.metadata import PackageNotFoundError

from sanic_adapters.adapters import RESTFramework
from sanic_adapters.routing import Routing


class TestAdapters:
    def test_autodiscover_when_package_is_passed_with_3_routes_then_resources_list_was_returned_with_3_routes(self):
        resources = RESTFramework.autodiscover("examples.qualnames")

        expected_resources = 2
        expected_routes = 3
        assert resources and len(resources) == expected_resources, f"Expected {expected_resources} resources, got {len(resources)}"
        assert len(Routing.routes()) == expected_routes, f"Expected {expected_routes} routes, got {len(Routing.routes())}"

    def test_autodiscover_when_package_not_exists_then_should_rise_exception_that_package_not_exists(self):
        with raises(PackageNotFoundError):
            RESTFramework.autodiscover("tests.not.existing.package")
import importlib
from utils.route_helpers import get_routes, get_route_functions


def test_route_functions_defined():
    routes = get_routes()
    for route in routes:
        route_functions = get_route_functions(route["path"])
        for function_desc in route_functions.values():
            module_path, method_name = function_desc.handler.split(".")
            module = importlib.import_module(module_path.replace("/", "."))
            route_definition_exists = getattr(module, method_name) is not None
            assert route_definition_exists

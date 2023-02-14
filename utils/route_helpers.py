import os, config
from typing import Dict

import yaml


class FunctionDefinition:
    def __init__(self, function_definition) -> None:
        self.function_definition = function_definition

    @property
    def handler(self) -> str:
        return self.function_definition["handler"]

    @property
    def path(self) -> str:
        return self.function_definition["events"][0]["httpApi"]["path"]

    @property
    def http_method(self) -> str:
        return self.function_definition["events"][0]["httpApi"]["method"]


def get_routes():
    routes = [
        dict(path=route.path, name=route.name)
        for route in os.scandir(os.path.join(config.ROOT_DIR, "routes"))
        if route.is_dir()
    ]
    return routes


def get_route_functions(route_path) -> Dict[str, FunctionDefinition]:
    with open(os.path.join(route_path, "route_config.yml")) as f:
        route_functions = yaml.safe_load(f.read())

    return {
        function_name: FunctionDefinition(function_desc)
        for function_name, function_desc in route_functions.items()
    }

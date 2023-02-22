import importlib
import os
import re
from typing import Any, List, get_args, get_origin
import config
import yaml

from utils.pydantic_helper import create_model

swagger_dataypes = {
    str: "string",
    int: "integer",
    float: "number",
    bool: "boolean",
    list: "array",
    object: "object",
}

PYDANTIC_VALIDATION_ERROR = {
    "description": "Pydantic Validation Error",
    "content": {
        "application/json": {
            "schema": {
                "title": "Validation Error",
                "type": "object",
                "properties": {
                    "detail": {
                        "title": "Detail",
                        "type": "array",
                        "items": {
                            "type": "object",
                            "title": "Pydantic Validation Error",
                            "properties": {
                                "field": {"title": "Field Name", "type": "string"},
                                "error": {"title": "Error Message", "type": "string"},
                            },
                        },
                    }
                },
            }
        }
    },
}


def get_route_configs(routes: List[str]) -> dict:
    route_configs = []
    for route in routes:
        with open(os.path.join(route["path"], "route_config.yml")) as f:
            route_functions = yaml.safe_load(f.read())
            for function_name, function_desc in route_functions.items():
                function_desc.update(route=route["name"])
                route_functions.update({function_name: function_desc})

            route_configs.append(route_functions)

    return route_configs


def parse_function_desc(function_name, function_desc) -> dict:
    path = function_desc["events"][0]["httpApi"]["path"]
    method = function_desc["events"][0]["httpApi"]["method"]
    tags = [function_desc["route"].capitalize()]
    summary = re.sub(r"(\w)([A-Z])", r"\1 \2", function_name)
    operation_id = function_desc["handler"].replace(".", "_").replace("/", "_")
    parameters = []
    components = {}
    request_body = None
    responses = {}
    module_path, method_name = function_desc["handler"].split(".")
    module = importlib.import_module(module_path.replace("/", "."))
    route_function = getattr(module, method_name)
    route_function_args = route_function._args
    require_auth = route_function_args["require_auth"]

    if route_function_args["query_parameters"] is not None:
        query_params_schema = create_model(
            route_function_args["query_parameters"]
        ).schema(ref_template="#/components/schemas/{model}")
        for param_name, param_desc in query_params_schema["properties"].items():
            parameter = {
                "name": param_name,
                "description": param_desc["title"],
                "in": "query",
                "schema": {"title": param_desc["title"], "type": param_desc["type"]},
            }
            if param_desc.get("default") is not None:
                parameter.get("schema").update(default=param_desc.get("default"))
            parameters.append(parameter)

    if route_function_args["path_parameters"] is not None:
        path_parameters_schema = create_model(
            route_function_args["path_parameters"]
        ).schema(ref_template="#/components/schemas/{model}")
        for param_name, param_desc in path_parameters_schema["properties"].items():
            parameter = {
                "name": param_name,
                "description": param_desc["title"],
                "in": "path",
                "schema": {"title": param_desc["title"], "type": param_desc["type"]},
            }
            if param_desc.get("default") is not None:
                parameter.get("schema").update(default=param_desc.get("default"))
            else:
                parameter.update(default=True)
            parameters.append(parameter)

    if route_function_args["body_model"] is not None:
        request_body = {
            "content": {
                "application/json": {
                    "schema": route_function_args["body_model"].schema(
                        ref_template="#/components/schemas/{model}"
                    )
                }
            }
        }

    if route_function_args["response_model"] is not None:
        if get_origin(route_function_args["response_model"]) is list:
            list_item_schema = get_args(route_function_args["response_model"])[
                0
            ].schema(ref_template="#/components/schemas/{model}")
            schema_definitions = list_item_schema.pop("definitions", {})
            schema = {
                "type": "array",
                "title": list_item_schema["title"],
                "items": list_item_schema,
            }
        else:
            schema = route_function_args["response_model"].schema(
                ref_template="#/components/schemas/{model}"
            )
            schema_definitions = schema.pop("definitions", {})

        responses.update(
            {
                "200": {
                    "description": "Successful operation",
                    "content": {
                        "application/json": {"schema": schema},
                    },
                },
                "422": PYDANTIC_VALIDATION_ERROR,
            }
        )
        components.update(schema_definitions)

    return dict(
        tags=tags,
        path=path,
        summary=summary,
        operation_id=operation_id,
        method=method,
        request_body=request_body,
        parameters=parameters,
        responses=responses,
        components=components,
        require_auth=require_auth,
    )


def parse_route_config(route_config: dict) -> dict:
    route_functions = []
    for function_name, function_desc in route_config.items():
        route_functions.append(parse_function_desc(function_name, function_desc))

    return route_functions


def parse_route_configs(route_configs: List[dict]) -> dict:
    function_schemas = []
    for route_config in route_configs:
        function_schemas.append(parse_route_config(route_config))

    return function_schemas


def generate_openapi_paths_and_components(route_configs: List[dict]) -> dict:
    openapi_paths = {}
    components = {}
    for route_config in route_configs:
        for function_config in route_config:
            if openapi_paths.get(function_config["path"]) is None:
                openapi_paths.update({function_config["path"]: {}})
            openapi_paths.get(function_config["path"]).update(
                {
                    function_config["method"]: {
                        "tags": function_config["tags"],
                        "summary": function_config["summary"],
                        "operationId": function_config["operation_id"],
                        "parameters": function_config["parameters"],
                        "responses": function_config["responses"],
                        "requestBody": function_config["request_body"],
                        "security": [{"Authentication": []}]
                        if function_config["require_auth"]
                        else None,
                    }
                }
            )
            if function_config.get("components"):
                components.update(function_config.get("components"))

    return openapi_paths, components


def get_openapi_schema():
    routes = [
        dict(path=route.path, name=route.name)
        for route in os.scandir(os.path.join(config.ROOT_DIR, "routes"))
        if route.is_dir() and "pycache" not in route.name
    ]

    route_configs = get_route_configs(routes)
    parsed_route_configs = parse_route_configs(route_configs)
    paths, schema_components = generate_openapi_paths_and_components(
        parsed_route_configs
    )
    schema = dict(
        openapi="3.0.2",
        info={"title": config.title, "version": "0.1.0"},
        paths=paths,
        components={
            "schemas": schema_components,
            "securitySchemes": {
                "Authentication": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                }
            },
        },
    )

    return schema

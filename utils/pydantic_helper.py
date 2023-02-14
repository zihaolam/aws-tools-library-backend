from typing import Dict, Any
from pydantic import create_model as pydantic_create_model


def create_model(schema: Dict[str, Any]):
    model_schema = {
        attr_name: attr_type if isinstance(attr_type, tuple) else (attr_type, ...)
        for attr_name, attr_type in schema.items()
    }

    return pydantic_create_model("placeholder_name", **model_schema)

from typing import Union, Set
from pynamodb.models import Model as PynamodbModel
from pydantic import BaseModel as PydanticModel
from exceptions import LambdaException


def map_attributes(
    source_obj: Union[PydanticModel, PynamodbModel],
    target_obj: PynamodbModel,
    exclude: Set[str] = set(),
    exclude_none: bool = True,
    additional_attributes: dict = {},
) -> PynamodbModel:
    """map pydantic or pynamodb model to target_obj(PynamodbModel), does not map pk, sk or type attributes
    Args:
        source_obj (Union[PydanticModel, PynamodbModel]): Source obj can be PynamodbModel or PydanticModel
        target_obj (PynamodbModel): Target PynamodbModel
        exclude (Set[str], optional): Fields to exclude from source obj. Defaults to set().
        exclude_none (bool, optional): Exclude fields which equal to None. Defaults to True.
        additional_attributes (dict, optional): Additional Attributes to be set. Defaults to {}.
    Returns:
        _type_: _description_
    """
    target_obj_attr_keys = list(target_obj.get_attributes().keys())

    if isinstance(source_obj, PydanticModel):
        intersected_attrs = {
            source_attr_key: source_attr_val
            for source_attr_key, source_attr_val in source_obj.dict(
                exclude=exclude, exclude_none=exclude_none
            ).items()
            if source_attr_key in target_obj_attr_keys
        }

        return target_obj._set_attributes(**intersected_attrs, **additional_attributes)

    if isinstance(source_obj, PynamodbModel):
        intersected_attrs = {
            source_attr_key: source_attr_val
            for source_attr_key, source_attr_val in source_obj.attribute_values.items()
            if source_attr_key in target_obj_attr_keys
        }

        intersected_attrs.pop("pk")
        intersected_attrs.pop("sk")
        intersected_attrs.pop("type")

        for attr in exclude:
            intersected_attrs.pop(attr)
        return target_obj._set_attributes(**intersected_attrs, **additional_attributes)

    return LambdaException(status_code=409, message="wrong parameter")

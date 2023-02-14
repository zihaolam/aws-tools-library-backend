from typing import Any, Generic, List, Optional, TypeVar, Union
from aws_lambda_powertools.utilities.parser import BaseModel
from pydantic.generics import GenericModel
from utils.to_camel import to_camel


class CustomBaseModel(BaseModel):
    class Config:
        orm_mode = True
        alias_generator = to_camel
        allow_population_by_field_name = True


class CustomGenericModel(GenericModel):
    class Config:
        orm_mode = True
        alias_generator = to_camel
        allow_population_by_field_name = True


DataType = TypeVar("DataType")


class ApiResponse(CustomGenericModel, Generic[DataType]):
    message: str
    data: DataType


class PaginatedList(CustomGenericModel, Generic[DataType]):
    items: List[DataType]
    last_evaluated_key: Any
    limit: int


class AuthTokenPayload(CustomBaseModel):
    sub: str
    email: str
    user_id: str
    exp: int
    auth_time: int

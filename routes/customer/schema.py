from typing import List
from schemas import CustomBaseModel
from pydantic import Field


class CustomerSchema(CustomBaseModel):
    pk: str
    sk: str = Field(alias="id")
    name: str


class CreateCustomerSchema(CustomBaseModel):
    name: str


class UpdateCustomerSchema(CustomBaseModel):
    name: str

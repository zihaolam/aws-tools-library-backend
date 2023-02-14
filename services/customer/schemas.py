from schemas import CustomBaseModel
from pydantic import Field

from services.customer.base import CustomerBase


class CreateCustomerSchema(CustomBaseModel):
    name: str


class UpdateCustomerSchema(CustomBaseModel):
    name: str


class CustomerSchemas:
    base = CustomerBase
    create = CreateCustomerSchema
    update = UpdateCustomerSchema

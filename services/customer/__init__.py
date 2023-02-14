from typing import Optional, Tuple
from models.constants import ModelTypes
from models.customer import CustomerModel
from utils.schema_helper import map_attributes
from .schemas import CustomerSchemas
from ulid import ULID


class CustomerService:
    model_type = ModelTypes.CUSTOMER
    customer_model = CustomerModel
    schema = CustomerSchemas

    @classmethod
    def generate_key(cls, customer_id: Optional[str] = str(ULID())) -> Tuple[str, str]:
        return cls.model_type, customer_id

    @classmethod
    def create(cls, body: CustomerSchemas.create) -> CustomerSchemas.base:
        new_customer = CustomerModel(*cls.generate_key())

        map_attributes(body, new_customer)

        new_customer.save()

        return new_customer

    @classmethod
    def find_all(cls, last_evaluated_key: Optional[str] = None) -> CustomerModel:
        return list(
            CustomerModel.query(
                ModelTypes.CUSTOMER, last_evaluated_key=last_evaluated_key
            )
        )

    @classmethod
    def update(
        cls, customer_id: str, body: CustomerSchemas.update
    ) -> CustomerSchemas.base:
        return CustomerModel.get(*cls.generate_key(customer_id))

from typing import List, Tuple
from routes.customer.schema import (
    CustomerSchema,
    CreateCustomerSchema,
    UpdateCustomerSchema,
)
from utils.lambda_helpers import lambda_handler, LambdaEvent

from services import CustomerService


@lambda_handler(response_model=List[CustomerSchema], require_auth=True)
def find_all(event: LambdaEvent, context):
    return CustomerService.find_all()


@lambda_handler(
    response_model=CustomerSchema, body_model=CreateCustomerSchema, require_auth=True
)
def create(event: LambdaEvent[CreateCustomerSchema], context):
    return CustomerService.create(
        CustomerService.schema.create(**event.parsed_body.dict())
    )


@lambda_handler(
    response_model=CustomerSchema,
    body_model=UpdateCustomerSchema,
    path_parameters={"customer_id": str},
    require_auth=True,
)
def update(event: LambdaEvent[UpdateCustomerSchema], context):
    return CustomerService.update(
        CustomerService.schema.update(**event.parsed_body.dict())
    )

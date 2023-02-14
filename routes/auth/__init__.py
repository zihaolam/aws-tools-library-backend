from schemas import CustomBaseModel
from utils.lambda_helpers import lambda_handler, LambdaEvent
from utils import auth_helper


class LoginBodyModel(CustomBaseModel):
    username: str
    password: str


@lambda_handler(body_model=LoginBodyModel)
def login(event: LambdaEvent[LoginBodyModel], context):
    return auth_helper.login(event.parsed_body.username, event.parsed_body.password)

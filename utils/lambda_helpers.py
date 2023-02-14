import json
from typing import Any, Dict, Generic, List, Optional, TypeVar
from pydantic import BaseModel as PydanticModel, ValidationError, parse_obj_as
from schemas import CustomBaseModel
from aws_lambda_powertools.utilities.data_classes import (
    APIGatewayProxyEventV2,
    event_source,
)
from utils.auth_helper import check_authenticated
from schemas import AuthTokenPayload
import logging
from exceptions import LambdaException, AuthException

from utils.pydantic_helper import create_model


class ApiResponse(CustomBaseModel):
    message: str
    body: Any
    statusCode: int


ParsedBodyType = TypeVar("ParsedBodyType")


class LambdaEvent(APIGatewayProxyEventV2, Generic[ParsedBodyType]):
    token_payload: Optional[AuthTokenPayload]
    parsed_body: ParsedBodyType
    parsed_path_parameters: CustomBaseModel
    parsed_query_parameters: CustomBaseModel


class ErrorResponseBody(CustomBaseModel):
    detail: Any


def response_body_parser(data, model=None) -> CustomBaseModel:
    if model is None:
        return data

    if isinstance(data, (List, list)):
        return [obj.dict(by_alias=True) for obj in parse_obj_as(model, data)]

    return parse_obj_as(model, data)


def lambda_response(
    status_code: int = 200, message: str = "Success", body: Optional[str] = None
):
    return ApiResponse(
        statusCode=status_code,
        message=message,
        body=body.json(by_alias=True)
        if isinstance(body, PydanticModel)
        else json.dumps(body),
    ).dict()


def pydantic_error_parser(errors):
    return [dict(field=error["loc"][-1], error=error["msg"]) for error in errors]


def auth_check(event):
    try:
        return check_authenticated(event)

    except AuthException as e:
        logging.exception(e)
        raise LambdaException(status_code=401, message="No authority")


def validate_body(event, body_model):
    try:
        if not event.json_body:
            logging.error("Invalid Body")
            raise LambdaException(message="Invalid Body", status_code=422)

    except TypeError as e:
        logging.exception(e)
        raise LambdaException(message="Invalid Body", status_code=422)

    try:
        return body_model(**event.json_body)

    except ValidationError as e:
        logging.exception(e)
        raise LambdaException(
            message=pydantic_error_parser(e.errors()),
            status_code=422,
        )


def validate_response(response_body, response_model):
    try:
        return response_body_parser(response_body, response_model)
    except ValidationError as e:
        logging.exception(e)
        raise LambdaException(
            message=pydantic_error_parser(e.errors()), status_code=422
        )


def lambda_handler(
    response_model: Optional[CustomBaseModel] = None,
    body_model: Optional[CustomBaseModel] = None,
    require_auth: Optional[bool] = False,
    path_parameters: Dict[str, Any] = None,
    query_parameters: Dict[str, Any] = None,
):
    def wrapper(handler):
        @event_source(data_class=APIGatewayProxyEventV2)
        def inner(event: APIGatewayProxyEventV2, context):
            try:
                if require_auth:
                    event.token_payload = auth_check(event)

                if body_model is not None:
                    # checking for empty or invalid (non-string) body
                    event.parsed_body = validate_body(event, body_model)

                if path_parameters is not None:
                    event.parsed_path_parameters = create_model(path_parameters)(
                        **event.path_parameters
                        if event.path_parameters is not None
                        else {}
                    )

                if query_parameters is not None:
                    event.parsed_query_parameters = create_model(query_parameters)(
                        **event.query_string_parameters
                        if event.query_string_parameters is not None
                        else {}
                    )

                response_body: Optional[dict] = handler(event, context)

                if response_model is not None:
                    validated_response = validate_response(
                        response_body, response_model
                    )
                    return lambda_response(body=validated_response)

                return lambda_response(body=response_body)

            except LambdaException as e:
                return lambda_response(
                    status_code=e.status_code,
                    body=ErrorResponseBody(detail=e.message),
                )

            except Exception as e:
                logging.exception(e)
                return lambda_response(
                    status_code=500, body=ErrorResponseBody(detail="Server Error")
                )

        inner._args = dict(
            response_model=response_model,
            body_model=body_model,
            require_auth=require_auth,
            path_parameters=path_parameters,
            query_parameters=query_parameters,
        )

        return inner

    return wrapper

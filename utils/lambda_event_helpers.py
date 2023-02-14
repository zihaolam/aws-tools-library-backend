from datetime import datetime
from schemas import CustomBaseModel

from urllib.parse import urlencode


def APIGatewayEvent(
    path: str = "",
    query_parameters: dict = {},
    method: str = "GET",
    path_parameters: dict = {},
    headers: dict = {},
    body: CustomBaseModel = CustomBaseModel(),
):
    event_date = datetime.now()
    raw_path = path
    for param_name, param_value in path_parameters.items():
        raw_path = raw_path.replace("{" + param_name + "}", param_value)
    event = {
        "version": "2.0",
        "routeKey": "$default",
        "rawPath": raw_path,
        "rawQueryString": urlencode(query_parameters),
        "cookies": ["cookie1", "cookie2"],
        "headers": headers,
        "queryStringParameters": query_parameters,
        "requestContext": {
            "accountId": "123456789012",
            "apiId": "api-id",
            "authentication": {
                "clientCert": {
                    "clientCertPem": "CERT_CONTENT",
                    "subjectDN": "www.example.com",
                    "issuerDN": "Example issuer",
                    "serialNumber": "a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1",
                    "validity": {
                        "notBefore": "May 28 12:30:02 2019 GMT",
                        "notAfter": "Aug  5 09:36:04 2021 GMT",
                    },
                }
            },
            "authorizer": {
                "jwt": {
                    "claims": {"claim1": "value1", "claim2": "value2"},
                    "scopes": ["scope1", "scope2"],
                }
            },
            "domainName": "id.execute-api.us-east-1.amazonaws.com",
            "domainPrefix": "id",
            "http": {
                "method": method,
                "path": raw_path,
                "protocol": "HTTP/1.1",
                "sourceIp": "192.168.0.1/32",
                "userAgent": "agent",
            },
            "requestId": "id",
            "routeKey": "$default",
            "stage": "$default",
            # "12/Mar/2020:19:03:58 +0000"
            "time": event_date.strftime("%d/%b/%Y:%T ") + "0800",
            "timeEpoch": event_date.timestamp(),
        },
        "body": body.json(),
        "pathParameters": path_parameters,
        "isBase64Encoded": False,
        "stageVariables": {"stageVariable1": "value1", "stageVariable2": "value2"},
    }

    return event

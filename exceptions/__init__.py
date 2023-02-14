import json
from typing import Union


class AuthException(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)


class LambdaException(Exception):
    def __init__(self, message: Union[dict, str], status_code):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

from utils.auth_helper import login, signup, verify_cognito_token


def signup_mock_account():
    signup("mock@mock.com", "mock_password")


def get_mock_auth_token():
    return login("mock@mock.com", "mock_password")


def get_mock_token_payload():
    return verify_cognito_token(get_mock_auth_token())

from exceptions import LambdaException
from create_table import run


if __name__ == "__main__":
    from utils.test_helpers import signup_mock_account

    try:
        run()
        signup_mock_account()
    except LambdaException as e:
        pass

import os
from dotenv import load_dotenv

title = "AWS Tools Library"
STAGE = os.getenv("STAGE")
BASEDIR = os.path.abspath(os.path.dirname(__file__))
ENV_FILE = ".env.dev" if STAGE == "dev" else ".env.prod"
ENV_PATH = os.path.join(BASEDIR, ENV_FILE)
REGION = os.getenv("REGION")
BUCKET_NAME = os.getenv("BUCKET_NAME")

print(f"Loading ENV from: {ENV_PATH}")
load_dotenv(ENV_PATH, override=True)

# COGNITO_USER_POOL_ID = os.getenv("COGNITO_USER_POOL_ID")
# COGNITO_APP_CLIENT_ID = os.getenv("COGNITO_APP_CLIENT_ID")

COGNITO_APP_CLIENT_ID = "5o0bl3u79ib0b8nttifhqpf6fm"
COGNITO_USER_POOL_ID = "ap-southeast-1_9iyG6shIe"
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

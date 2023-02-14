from fastapi import HTTPException
from bcrypt import hashpw, gensalt, checkpw


def encrypt(password: str) -> str:
    return hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')


def verify_password(password: str, challenge_password: bytes):
    if not checkpw(password.encode('utf-8'), challenge_password.encode("utf-8")):
        raise HTTPException(
            status_code=401, detail="Username and password do not match")

    return

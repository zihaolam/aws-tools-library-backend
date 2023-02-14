from typing import List


def generate_key(*args: List[str]) -> str:
    return "__".join(args)


def strip_key(key: str, index=1) -> str:
    return key.split("__")[index]

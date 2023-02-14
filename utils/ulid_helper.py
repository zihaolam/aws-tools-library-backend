from ulid import ULID

class ULIDHelper(ULID):
    def new(self) -> str:
        return str(ULID())


ULID = ULIDHelper()
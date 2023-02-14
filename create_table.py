from models.base import BaseModel


def run():
    BaseModel.create_table()


if __name__ == "__main__":
    run()

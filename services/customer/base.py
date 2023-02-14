from schemas import CustomBaseModel
from pydantic import Field


class CustomerBase(CustomBaseModel):
    pk: str
    sk: str = Field(alias="id")
    name: str

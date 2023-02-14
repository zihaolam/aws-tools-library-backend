from typing import Optional
from schemas import CustomBaseModel
from pydantic import Field

from services.customer.base import CustomerBase


class CreateStorageUtilizationSchema(CustomBaseModel):
    year: str
    month: str
    service: str
    usage: float
    customer_id: str

    @staticmethod
    def fields_to_exclude():
        return {"year", "month"}


class CreateCumulativeStorageUtilizationSchema(CustomBaseModel):
    year: str
    month: str
    usage: float
    customer_id: str

    @staticmethod
    def fields_to_exclude():
        return {"year", "month"}


class StorageUtilizationBaseSchema(CustomBaseModel):
    pk: str = Field(alias="id")
    sk: str = Field(alias="date")
    usage: float
    service: str
    customer_id: str
    customer_name: str


class CumulativeStorageUtilizationBaseSchema(CustomBaseModel):
    pk: str = Field(alias="id")
    sk: str = Field(alias="date")
    usage: float
    customer_id: str
    customer_name: str


class CumulativeStorageUtilizationFilterSchema(CustomBaseModel):
    year: Optional[str]
    month: Optional[str]


class StorageUtilizationSchemas:
    base = StorageUtilizationBaseSchema
    create = CreateStorageUtilizationSchema
    cumulative = CumulativeStorageUtilizationBaseSchema
    create_cumulative = CreateCumulativeStorageUtilizationSchema
    find_cumulative_filter = CumulativeStorageUtilizationFilterSchema

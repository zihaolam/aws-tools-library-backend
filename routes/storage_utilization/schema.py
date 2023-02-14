from typing import List
from schemas import CustomBaseModel


class StorageUtilizationSchema(CustomBaseModel):
    service: str
    usage: str
    customer_name: str
    customer_id: str


class ExtractStorageUtilizationSchema(CustomBaseModel):
    files: List[str]
    customer_id: str
    year: str
    month: str

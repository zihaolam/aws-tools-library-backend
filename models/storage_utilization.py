from .base import BaseModel
from .constants import ModelTypes
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, MapAttribute


class StorageUtilizationModel(BaseModel, discriminator=ModelTypes.STORAGE_UTILIZATION):
    pk = UnicodeAttribute(default_for_new=ModelTypes.STORAGE_UTILIZATION, hash_key=True)
    service = UnicodeAttribute()
    usage = NumberAttribute()
    customer_id = UnicodeAttribute()
    customer_name = UnicodeAttribute()


class CumulativeStorageUtilizationModel(
    BaseModel, discriminator=ModelTypes.CUMULATIVE_STORAGE_UTILIZATION
):
    pk = UnicodeAttribute(
        default_for_new=ModelTypes.CUMULATIVE_STORAGE_UTILIZATION, hash_key=True
    )
    usage = NumberAttribute()
    customer_id = UnicodeAttribute()
    customer_name = UnicodeAttribute()

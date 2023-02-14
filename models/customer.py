from models.base import BaseModel
from .constants import ModelTypes
from pynamodb.attributes import UnicodeAttribute, MapAttribute


class CustomerModel(BaseModel, discriminator=ModelTypes.CUSTOMER):
    pk = UnicodeAttribute(hash_key=True, default_for_new=ModelTypes.CUSTOMER)
    name = UnicodeAttribute()

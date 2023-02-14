from typing import Set
from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute,
    DiscriminatorAttribute,
)
from pynamodb.indexes import AllProjection, GlobalSecondaryIndex
import config


class SortKeyIndex(GlobalSecondaryIndex):
    class Meta:
        index_name = "sort-key-index"
        read_capacity_units = 5
        write_capacity_units = 5
        projection = AllProjection()

    sk = UnicodeAttribute(hash_key=True)
    pk = UnicodeAttribute(range_key=True)


class CustomerIdIndex(GlobalSecondaryIndex):
    class Meta:
        index_name = "customer-id-index"
        read_capacity_units = 5
        write_capacity_units = 5
        projection = AllProjection()

    customer_id = UnicodeAttribute(hash_key=True)
    sk = UnicodeAttribute(range_key=True)


class BaseModel(Model):
    class Meta:
        if config.STAGE == "staging":
            table_name = "STORAGE_CALCULATION_TABLE_STAGING"
        else:
            table_name = "STORAGE_CALCULATION_TABLE"
        region = "ap-southeast-1"
        read_capacity_units = 25
        write_capacity_units = 25
        if config.STAGE == "dev":
            host = "http://localhost:8392"

    pk = UnicodeAttribute(hash_key=True)
    sk = UnicodeAttribute(range_key=True)
    sk_index = SortKeyIndex()
    type = DiscriminatorAttribute()
    customer_id = UnicodeAttribute(null=True)
    customer_id_index = CustomerIdIndex()

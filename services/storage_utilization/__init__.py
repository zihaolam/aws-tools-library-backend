from typing import Tuple
from models.constants import ModelTypes
from models.customer import CustomerModel
from models.storage_utilization import (
    StorageUtilizationModel,
    CumulativeStorageUtilizationModel,
)
from utils.schema_helper import map_attributes
from .schemas import StorageUtilizationSchemas
from ulid import ULID


class StorageUtilizationService:
    storage_utilization_model = StorageUtilizationModel
    cumulative_storage_utilization_model = CumulativeStorageUtilizationModel
    schema = StorageUtilizationSchemas

    @classmethod
    def generate_key(cls, year: str, month: str) -> Tuple[str, str]:
        return ModelTypes.STORAGE_UTILIZATION, year + month + "__" + str(ULID())

    @classmethod
    def generate_cumu_key(cls, year: str, month: str) -> Tuple[str, str]:
        return ModelTypes.CUMULATIVE_STORAGE_UTILIZATION, year + month + "__" + str(
            ULID()
        )

    @classmethod
    def create(
        cls, body: StorageUtilizationSchemas.create
    ) -> StorageUtilizationSchemas.base:
        new_storage_utilization_record = cls.storage_utilization_model(
            *cls.generate_key(body.year, body.month)
        )

        customer = CustomerModel.get(ModelTypes.CUSTOMER, body.customer_id)

        map_attributes(
            body, new_storage_utilization_record, exclude=body.fields_to_exclude()
        )

        new_storage_utilization_record.customer_id = customer.sk
        new_storage_utilization_record.customer_name = customer.name

        new_storage_utilization_record.customer_id = customer.sk
        new_storage_utilization_record.customer_name = customer.name

        new_storage_utilization_record.save()

        return new_storage_utilization_record

    @classmethod
    def create_cumulative(
        cls, body: StorageUtilizationSchemas.create_cumulative
    ) -> StorageUtilizationSchemas.cumulative:
        new_cumulative_storage_utilization_record = (
            cls.cumulative_storage_utilization_model(
                *cls.generate_cumu_key(body.year, body.month)
            )
        )

        customer = CustomerModel.get(ModelTypes.CUSTOMER, body.customer_id)

        map_attributes(
            body,
            new_cumulative_storage_utilization_record,
            exclude=body.fields_to_exclude(),
        )

        new_cumulative_storage_utilization_record.customer_id = customer.sk
        new_cumulative_storage_utilization_record.customer_name = customer.name

        new_cumulative_storage_utilization_record.save()

        return new_cumulative_storage_utilization_record

    @classmethod
    def find_cumulative(cls, filters: StorageUtilizationSchemas.find_cumulative_filter):
        return list(
            CumulativeStorageUtilizationModel.query(
                ModelTypes.CUMULATIVE_STORAGE_UTILIZATION,
                range_key_condition=cls.cumulative_storage_utilization_model.sk.startswith(
                    filters.year + filters.month
                )
                if filters.year and filters.month
                else None,
            )
        )

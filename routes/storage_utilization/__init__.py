from typing import List, Tuple
from .schema import (
    StorageUtilizationSchema,
    ExtractStorageUtilizationSchema,
)

from utils.lambda_helpers import lambda_handler, LambdaEvent
from utils.s3_helper import s3_upload
from utils.storage_utilization_extract import transform_s3_files

from services import StorageUtilizationService


@lambda_handler(
    response_model=List[StorageUtilizationSchema],
    body_model=ExtractStorageUtilizationSchema,
    require_auth=True,
)
def extract(event: LambdaEvent[ExtractStorageUtilizationSchema], context):
    def gen_bucket_key_pair(bucket_key_pair: Tuple[str, str]):
        bucket_name, file_key = bucket_key_pair
        return dict(bucket_name=bucket_name, file_key=file_key)

    bucket_key_pairs = [
        gen_bucket_key_pair(s3_upload(base64_file))
        for base64_file in event.parsed_body.files
    ]

    transformed_files = transform_s3_files(
        [
            dict(bucket_name=filepath["bucket_name"], file_key=filepath["file_key"])
            for filepath in bucket_key_pairs
        ]
    )

    results = [
        StorageUtilizationService.create(
            StorageUtilizationService.schema.create(
                year=event.parsed_body.year,
                month=event.parsed_body.month,
                service=transformed_file["service"],
                usage=transformed_file["usage"],
                customer_id=event.parsed_body.customer_id,
            )
        )
        for transformed_file in transformed_files
    ]

    StorageUtilizationService.create_cumulative(
        StorageUtilizationService.schema.create_cumulative(
            year=event.parsed_body.year,
            month=event.parsed_body.month,
            usage=sum(
                [transformed_file["usage"] for transformed_file in transformed_files]
            ),
            customer_id=event.parsed_body.customer_id,
        )
    )

    return results


@lambda_handler(
    response_model=List[StorageUtilizationService.schema.cumulative],
    query_parameters=dict(year=(str, None), month=(str, None)),
    require_auth=True,
)
def find_cumulative_records(event: LambdaEvent, context):
    return StorageUtilizationService.find_cumulative(
        filters=StorageUtilizationService.schema.find_cumulative_filter(
            year=event.parsed_query_parameters.year,
            month=event.parsed_query_parameters.month,
        )
    )

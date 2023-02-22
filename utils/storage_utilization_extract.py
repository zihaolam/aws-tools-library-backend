from typing import Any, Dict, List
from math import log10, floor
import csv

from utils.s3_helper import S3File

BucketKeyPair = Dict[str, str]


def round_to_sf(x, n):
    return round(x, -int(floor(log10(abs(x)))) + n - 1)


def csv_to_json(csvFile):
    data = []
    with open(csvFile) as csvfile:
        csv_data = csv.DictReader(csvfile)
        for rows in csv_data:
            data.append(rows)  # Appending all the csv rows

    return data


def read_files_from_s3(s3_paths: List[BucketKeyPair]) -> List[Any]:
    data = []

    for s3_path in s3_paths:
        with S3File(s3_path["bucket_name"], s3_path["file_key"]) as f:
            csv_data = csv_to_json(f)
            data.extend(csv_data)

    return data


def transform(s3_billing_csv: List[str]):
    bill_map: Dict[str, float] = {}
    for row in s3_billing_csv:
        if "storage" in row["Charge description"]:
            service = (
                "Amazon Elastic Block Store"
                if row["Service"] == "Amazon Elastic Compute Cloud"
                else row["Service"]
            )
            if service not in bill_map:
                bill_map[service] = 0
            bill_map[service] += float(row["Usage amount"])

    return [dict(service=service, usage=usage) for service, usage in bill_map.items()]


def transform_s3_files(s3_paths: List[BucketKeyPair]):
    csvs = read_files_from_s3(s3_paths)
    return transform(csvs)

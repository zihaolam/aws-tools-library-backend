import os
from typing import Generator, Tuple
from datauri import DataURI
import traceback
import boto3
import config
from uuid import uuid4

s3 = boto3.resource("s3")
bucket_name = config.BUCKET_NAME
# where the file will be uploaded, if you want to upload the file to folder use 'Folder Name/FileName.jpeg'


# make sure there is no data:image/jpeg;base64 in the string that returns
def s3_upload(base64_file: str) -> Tuple[str, str]:
    file_key = str(uuid4())
    obj = s3.Object(bucket_name, file_key)
    base64_data = DataURI(base64_file)
    obj.put(Body=base64_data.data)
    return bucket_name, file_key


class S3File:
    temp_path = None

    def __init__(self, bucket_name: str, file_key: str):
        self.bucket_name = bucket_name
        self.file_key = file_key

    def __enter__(self):
        self.temp_path = f"tmp/{uuid4()}"
        s3.meta.client.download_file(self.bucket_name, self.file_key, self.temp_path)
        return self.temp_path

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)
        if self.temp_path is not None:
            os.unlink(self.temp_path)

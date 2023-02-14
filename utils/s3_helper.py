from typing import Tuple
from datauri import DataURI
import base64
import boto3
import config
from uuid import uuid4

s3 = boto3.resource('s3')
bucket_name = config.BUCKET_NAME
#where the file will be uploaded, if you want to upload the file to folder use 'Folder Name/FileName.jpeg'

#make sure there is no data:image/jpeg;base64 in the string that returns
def s3_upload(base64_file: str) -> Tuple[str, str]:
    file_key = str(uuid4())
    obj = s3.Object(bucket_name, file_key)
    base64_data = DataURI(base64_file)
    obj.put(Body=base64_data.data)
    return bucket_name, file_key
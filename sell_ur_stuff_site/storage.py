import os
from storages.backends.s3boto3 import S3Boto3Storage

print("Loading storage.py")


class CustomS3Boto3Storage(S3Boto3Storage):
    def __init__(self):
        print("Initializing CustomS3Boto3Storage")
        super().__init__(
            access_key=os.getenv("AWS_ACCESS_KEY_ID"),
            secret_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            bucket_name="sellyourtuff",
            region_name="eu-west-1",
            querystring_auth=False,
            file_overwrite=False,
        )
        print("CustomS3Boto3Storage initialized successfully")


print("Finished loading storage.py")

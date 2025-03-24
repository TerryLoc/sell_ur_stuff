import os
from storages.backends.s3boto3 import S3Boto3Storage

print("Loading storage.py")

try:

    class CustomS3Boto3Storage(S3Boto3Storage):
        def __init__(self):
            print("Initializing CustomS3Boto3Storage")
            try:
                super().__init__(
                    access_key=os.getenv("AWS_ACCESS_KEY_ID"),
                    secret_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                    bucket_name="sellyourtuff",
                    region_name="eu-west-1",
                    querystring_auth=False,
                    file_overwrite=False,
                )
                print("CustomS3Boto3Storage initialized successfully")
            except Exception as e:
                print(f"Failed to initialize CustomS3Boto3Storage: {e}")
                raise

except Exception as e:
    print(f"Failed to define CustomS3Boto3Storage: {e}")
    raise

print("Finished loading storage.py")

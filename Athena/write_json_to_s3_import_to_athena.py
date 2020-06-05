from boto3.session import Session
import logging
import json
import os

# Update the root logger to get messages at DEBUG and above
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger("botocore").setLevel(logging.CRITICAL)
logging.getLogger("boto3").setLevel(logging.CRITICAL)
logging.getLogger("urllib3.connectionpool").setLevel(logging.CRITICAL)

DATA_BUCKET = os.getenv("DATA_BUCKET")

#s3 = boto3.client("s3")
s3 = Session(profile_name="default").client("s3")


def write_to_s3(data, s3_key, bucket=DATA_BUCKET, encrypt_mode=None, kms_key=None):
    """
    :param encrypt_mode: None, AES256, or aws:kms
    :param kms_key: None or arn or alias arn
    """

    # Athena requires output each item to separate line
    # No outer bracket, no commas at the end of the line
    # {"k1": "v1"}
    # {"k1": "v2"}
    bdata = "\n".join([json.dumps(item) for item in data])
    
    params = {
        "Body": data,
        "Key": s3_key,
        "Bucket": bucket,
        "ACL": "bucket-owner-full-control",
    }
    if encrypt_mode is not None:
        params["ServerSideEncryption"] = encrypt_mode
    if kms_key is not None:
        params["SSEKMSKeyId"] = kms_key
    
    return s3.put_object(**params)


data = [
    {"k1": "v1"},
    {"k1": "v2"},
]


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


def write_to_s3(data, key):
    bdata = "\n".join([json.dumps(item) for item in data])
    s3.put_object(
        Body=bdata, Key=key, Bucket=DATA_BUCKET, ACL="bucket-owner-full-control",
        # TODO enforce encryption when KMS key is ready
        # ServerSideEncryption="aws:kms", SSEKMSKeyId="TODO-KMS_ALIAS_ARN",
    )


data = [
    {"k1": "v1"},
    {"k1": "v2"},
]

# Athena requires output each item to separate line
# No outer bracket, no commas at the end of the line
# {"k1": "v1"}
# {"k1": "v2"}

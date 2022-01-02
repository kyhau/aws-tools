"""
List details of a bucket or all buckets accessible by the profiles in .aws/.
"""
import json
import logging

import fire
from botocore.exceptions import ClientError
from helper.aws import AwsApiHelper

logging.getLogger().setLevel(logging.DEBUG)


class Helper(AwsApiHelper):
    def process_request(self, session, account_id, region, kwargs):
        client = session.client("s3", region_name=region)
        target_bucket = kwargs.get("Bucket")

        def rm_meta(response):
            del response["ResponseMetadata"]
            return response

        for item in [{"Name": target_bucket}] if target_bucket else client.list_buckets()["Buckets"]:
            bucket = item["Name"]
            data = {
                item["Name"]: {
                    "account_id": account_id,
                    "accelerate_configuration": rm_meta(client.get_bucket_accelerate_configuration(Bucket=bucket)),
                    "acl": rm_meta(client.get_bucket_acl(Bucket=bucket)),
                    "cors": self.get_bucket_cors(client, bucket),
                    "encryption": self.get_bucket_encryption(client, bucket),
                    "lifecycle_configuration": self.get_bucket_lifecycle_configuration(client, bucket),
                    "location": client.get_bucket_location(Bucket=bucket)["LocationConstraint"],
                    "logging": rm_meta(client.get_bucket_logging(Bucket=bucket)),
                    "notification_configuration": rm_meta(client.get_bucket_notification_configuration(Bucket=bucket)),
                    "policy": self.get_bucket_policy(client, bucket),
                    "policy_status": self.get_bucket_policy_status(client, bucket),
                    "replication": self.get_bucket_replication(client, bucket),
                    "request_payment": client.get_bucket_request_payment(Bucket=bucket)["Payer"],
                    "tagging": self.get_bucket_tagging(client, bucket),
                    "versioning": rm_meta(client.get_bucket_versioning(Bucket=bucket)),
                    "website": self.get_bucket_website(client, bucket),
                }
            }
            print(json.dumps(data, indent=2, sort_keys=True))
            if kwargs.get("Bucket"):
                return True

    def get_bucket_cors(self, client, bucket):
        try:
            return client.get_bucket_cors(Bucket=bucket)["CORSRules"]
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchCORSConfiguration":
                pass

    def get_bucket_encryption(self, client, bucket):
        try:
            return client.get_bucket_encryption(Bucket=bucket)["ServerSideEncryptionConfiguration"]
        except ClientError as e:
            if e.response["Error"]["Code"] == "ServerSideEncryptionConfigurationNotFoundError":
                pass

    def get_bucket_lifecycle_configuration(self, client, bucket):
        try:
            return client.get_bucket_lifecycle_configuration(Bucket=bucket)["Rules"]
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchLifecycleConfiguration":
                pass

    def get_bucket_replication(self, client, bucket):
        try:
            return client.get_bucket_replication(Bucket=bucket)["ReplicationConfiguration"],
        except ClientError as e:
            if e.response["Error"]["Code"] == "ReplicationConfigurationNotFoundError":
                pass

    def get_bucket_policy(self, client, bucket):
        try:
            return client.get_bucket_policy(Bucket=bucket)["Policy"],
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchBucketPolicy":
                pass

    def get_bucket_policy_status(self, client, bucket):
        try:
            return client.get_bucket_policy_status(Bucket=bucket)["PolicyStatus"],
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchBucketPolicy":
                pass

    def get_bucket_tagging(self, client, bucket):
        try:
            return client.get_bucket_tagging(Bucket=bucket)["TagSet"],
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchTagSet":
                pass

    def get_bucket_website(self, client, bucket):
        try:
            return client.get_bucket_website(Bucket=bucket),
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchWebsiteConfiguration":
                pass


def main(bucket=None, profile=None, region="ap-southeast-2"):
    kwargs = {"Bucket": bucket} if bucket else {}
    Helper().start(profile, region, "s3", kwargs)


if __name__ == "__main__":
    fire.Fire(main)

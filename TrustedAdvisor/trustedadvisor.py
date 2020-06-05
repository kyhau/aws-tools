from abc import ABC, abstractmethod
from boto3.session import Session
from botocore.exceptions import ClientError
import boto3
import logging
import json
import os
from time import time

# Update the root logger to get messages at DEBUG and above
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger("botocore").setLevel(logging.CRITICAL)
logging.getLogger("boto3").setLevel(logging.CRITICAL)
logging.getLogger("urllib3.connectionpool").setLevel(logging.CRITICAL)

logging.info(f"boto3.__version__: {boto3.__version__}")

DATA_BUCKET = os.getenv("DATA_BUCKET")

#s3 = boto3.client("s3")
s3 = Session(profile_name="default").client("s3")


def write_to_s3(data, key):
    # Athena requires output each item to separate line
    bdata = "\n".join([json.dumps(item) for item in data])
    s3.put_object(
        Body=bdata, Key=key, Bucket=DATA_BUCKET, ACL="bucket-owner-full-control",
        # TODO enforce encryption when KMS key is ready
        # ServerSideEncryption="aws:kms", SSEKMSKeyId="TODO-KMS_ALIAS_ARN",
    )


def get_tag_value(tags, tag, default="Unspecified", to_lower=False):
    for t in tags:
        if t["Key"] == tag:
            return t["Value"].lower() if to_lower else t["Value"]
    return default


def request_data(client, func_name, result_key=None):
    for page in client.get_paginator(func_name).paginate().result_key_iters():
        for item in page:
            if result_key is None:
                yield item
            else:
                for subitem in item[result_key]:
                    yield subitem


class Helper(ABC):
    def __init__(self, name, request_func, result_key=None):
        self._name = name
        self._request_func = request_func
        self._result_key = result_key
        self._client = None
        self._region = None
        self._account_id = None

    @property
    def name(self):
        return self._name
    
    @abstractmethod
    def process_response(self, item):
        pass
    
    def process_request(self, session, region, account_id):
        self._client = session.client(self.name, region_name=region)
        self._region, self._account_id = region, account_id
        ret = []
        for item in request_data(self._client, self._request_func, self._result_key):
            data = self.process_response(item)
            if data:
                data.update({"AccountId": account_id, "Region": region})
                ret.append(data)
        return ret
    
    def get_tags(self, item):
        return item.get("Tags", [])


class EC2Helpher(Helper):
    def __init__(self):
        super().__init__("ec2", "describe_instances", "Instances")

    def process_response(self, item):
        tags = self.get_tags(item)
        return {
            "Service": self.name,
            "Id": item["InstanceId"],
            "FromASG": get_tag_value(tags, "aws:autoscaling:groupName") != "Unspecified",
        }


class ElbHelper(Helper):
    def __init__(self, v2=False):
        super().__init__("elbv2" if v2 else "elb", "describe_load_balancers")
    
    def get_tags(self, item):
        if self.name == "elb":
            return self._client.describe_tags(LoadBalancerNames=[item["LoadBalancerName"]])["TagDescriptions"][0]["Tags"]
        elif self.name == "elbv2":
            return self._client.describe_tags(ResourceArns=[item["LoadBalancerArn"]])["TagDescriptions"][0]["Tags"]

    def process_response(self, item):
        tags = self.get_tags(item)
        return {
            "Service": self.name,
            "Type": item["Type"] if self.name == "elbv2" else "classic",
            "Id": item["LoadBalancerName"],
            "MultiAZ": len(item["AvailabilityZones"]) > 0,
            "PublicFacing": item["Scheme"] == "internet-facing",
        }


class ElasticsearchHelper(Helper):
    def __init__(self):
        super().__init__("es", None)

    def get_tags(self, item):
        return self._client.list_tags(ARN=item["ARN"])["TagList"]
    
    def process_response(self, item):
        tags = self.get_tags(item)
        return {
            "Service": self.name,
            "Id": item.get("DomainName"),
            "AutoBackup": item.get("SnapshotOptions", {}).get("AutomatedSnapshotStartHour", 0) > 0,
            "MultiAZ": len(item["VPCOptions"]["AvailabilityZones"]) > 0,
            "EncryptedAtRest": item["EncryptionAtRestOptions"].get("Enabled", False),
        }
    
    def process_request(self, session, region, account_id):
        self._client = session.client(self.name, region_name=region)
        self._region, self._account_id = region, account_id
        ret = []
        domain_names = [x["DomainName"] for x in self._client.list_domain_names()["DomainNames"]]
        if domain_names:
            for item in self._client.describe_elasticsearch_domains(DomainNames=domain_names)["DomainStatusList"]:
                data = self.process_response(item)
                if data:
                    data.update({"AccountId": account_id, "Region": region})
                    ret.append(data)
        return ret


class EbsHelper(Helper):
    def __init__(self):
        super().__init__("ec2", "describe_volumes")
    
    def process_response(self, item):
        if "attached" in str(item.get("Attachments", {})):
            tags = self.get_tags(item)
            return {
                "Service": "ebs",
                "Id": item["VolumeId"],
                "EncryptedAtRest": item["Encrypted"],
            }


class EfsHelper(Helper):
    def __init__(self):
        super().__init__("efs", "describe_file_systems")
    
    def get_tags(self, item):
        return self._client.describe_tags(FileSystemId=item["FileSystemId"])["Tags"]
    
    def process_response(self, item):
        tags = self.get_tags(item)
        return {
            "Service": self.name,
            "Id": item["FileSystemId"],
            "MultiAZ": True,  # Always true
            "EncryptedAtRest": item["Encrypted"],
        }


class S3Helper(Helper):
    def __init__(self):
        super().__init__("s3", "list_buckets")
    
    def get_tags(self, item):
        try:
            return self._client.get_bucket_tagging(Bucket=item).get("TagSet", [])
        except:
            return []
    
    def get_sse(self, item):
        try:
            s = str(self._client.get_bucket_encryption(Bucket=item).get("ServerSideEncryptionConfiguration", {}))
            return "AES256" in s or "aws:kms" in s
        except:
            return False
    
    def process_response(self, item):
        tags = self.get_tags(item)
        return {
            "Service": self.name,
            "Id": item,
            "EncryptedAtRest": self.get_sse(item),
        }
    
    def process_request(self, session, region, account_id):
        self._client = session.client(self.name, region_name=region)
        self._region, self._account_id = region, account_id
        ret = []
        for bucket_name in [x["Name"] for x in self._client.list_buckets()["Buckets"]]:
            data = self.process_response(bucket_name)
            if data:
                data.update({"AccountId": account_id, "Region": region})
                ret.append(data)
        return ret


class RdsHelper(Helper):
    """
    Neptune, DocumentDB information are also returned from rds.describe_db_instances.
    Engine: aurora, aurora-mysql, aurora-postgresql, mariadb, oracle-*, postgres, sqlserver-*, neptune, docdb
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Client.describe_db_instances
    """
    def __init__(self):
        super().__init__("rds", "describe_db_instances")

    def get_tags(self, item):
        return self._client.list_tags_for_resource(ResourceName=item["DBInstanceArn"])["TagList"]

    def process_response(self, item):
        if item.get("DBInstanceStatus") == "available":
            tags = self.get_tags(item)
            return {
                "Service": item["Engine"] if item["Engine"] in ["neptune", "docdb"] else "rds",
                "Engine": item["Engine"],
                "Id": item["DBInstanceIdentifier"],
                "AutoBackup": item.get("BackupRetentionPeriod", 0) > 0,
                "MultiAZ": item["MultiAZ"],
                "EncryptedAtRest": item["StorageEncrypted"],
                "PublicFacing": item["PubliclyAccessible"],
            }


class ElastiCacheHelper(Helper):
    def __init__(self):
        super().__init__("elasticache", "describe_cache_clusters")

    def get_tags(self, item):
        arn = item.get("ARN", f"arn:aws:elasticache:{self._region}:{self._account_id}:cluster:{item['CacheClusterId']}")
        return self._client.list_tags_for_resource(ResourceName=arn)["TagList"]

    def process_response(self, item):
        if item.get("CacheClusterStatus") == "available":
            tags = self.get_tags(item)
            return {
                "Service": self.name,
                "Engine": item["Engine"],    # memcached or redis
                "Id": item["CacheClusterId"],
                "AutoBackup": item.get("SnapshotRetentionLimit", 0) > 0,
                "MultiAZ": item["PreferredAvailabilityZone"] == "Multiple",
                "EncryptedAtRest": item["AtRestEncryptionEnabled"],
            }


class RedshiftHelper(Helper):
    def __init__(self):
        super().__init__("redshift", "describe_clusters")

    def process_response(self, item):
        if item.get("ClusterAvailabilityStatus") != "Unavailable":
            tags = self.get_tags(item)
            return {
                "Service": self.name,
                "Engine": self.name,
                "Id": item.get("ClusterIdentifier"),
                "AutoBackup": item.get("AutomatedSnapshotRetentionPeriod", 0) > 0,
                "MultiAZ": False,    # Redshift only supports Single-AZ deployments (last checked 2020-06-02)
                "EncryptedAtRest": item["Encrypted"],
                "PublicFacing": item["PubliclyAccessible"],

            }


class DynamoDBHelper(Helper):
    def __init__(self):
        super().__init__("dynamodb", "list_tables")

    def get_tags(self, item):
        return self._client.list_tags_of_resource(
            ResourceArn=f"arn:aws:dynamodb:{self._region}:{self._account_id}:table/{item}")["Tags"]

    def process_response(self, item):
        cb = self._client.describe_continuous_backups(TableName=item)    # item == table_name
        piir = cb["ContinuousBackupsDescription"]["PointInTimeRecoveryDescription"]["PointInTimeRecoveryStatus"] == "ENABLED"
        tags = self.get_tags(item)
        return {
            "Service": self.name,
            "Engine": self.name,
            "Id": item,
            "AutoBackup": piir,
            "MultiAZ": True,             # Always true
            "EncryptedAtRest": True,     # Always on
        }


class TrustedAdvisorHelper(Helper):
    def __init__(self):
        super().__init__("support", "")

    def process_response(self, item):
        result = self._client.describe_trusted_advisor_check_result(checkId=item["id"], language="en")["result"]
        if result["status"] in ["error", "warning"]:  # "ok" (green), "warning" (yellow), "error" (red), "not_available"
            return {
                "Service": self.name,
                "Category": item["category"],
                "Id": item["id"],
                "Name": item["name"],
                "ResourcesFlaggedCnt": result.get("resourcesSummary", {}).get("resourcesFlagged", 0),
                "ResourcesFlagged": result.get("flaggedResources", []),
            }

    def process_request(self, session, region, account_id):
        self._client = session.client(self.name, region_name=region)
        self._region, self._account_id = region, account_id
        ret = []
        for item in self._client.describe_trusted_advisor_checks(language="en")["checks"]:
            if (item["category"], item["name"]) in [
                ("fault_tolerance", "Auto Scaling Group Resources"),
                ("security", "Amazon EBS Public Snapshots"),
                ("security", "Amazon RDS Public Snapshots"),
                ("security", "Amazon S3 Bucket Permissions"),
                ("security", "CloudFront Custom SSL Certificates in the IAM Certificate Store"),
                ("security", "CloudFront SSL Certificate on the Origin Server"),
                ("security", "IAM Access Key Rotation"),
                ("service_limits", "EC2 On-Demand Instances"),
            ]:
                data = self.process_response(item)
                if data:
                    data.update({"AccountId": account_id})
                    ret.append(data)
        return ret



def process_account(session, account_id):
    service_groups = [
        (f"cloud/s3/s3_{account_id}.json", [S3Helper()], ["ap-southeast-2"]),
        (f"cloud/database/rds_{account_id}.json", [RdsHelper()], None),
        (f"cloud/database/dynamodb_{account_id}.json", [DynamoDBHelper()], None),
        (f"cloud/database/elasticache_{account_id}.json", [ElastiCacheHelper()], None),
        (f"cloud/database/redshift_{account_id}.json", [RedshiftHelper()], None),
        (f"cloud/ec2/ec2_{account_id}.json", [EC2Helpher()], None),
        (f"cloud/ebs/ebs_{account_id}.json", [EbsHelper()], None),
        (f"cloud/efs/efs_{account_id}.json", [EfsHelper()], None),
        (f"cloud/elb/elb_{account_id}.json", [ElbHelper(), ElbHelper(v2=True)], None),
        (f"cloud/es/es_{account_id}.json", [ElasticsearchHelper()], None),
        (f"cloud/trustedadvisor/trustedadvisor_{account_id}.json", [TrustedAdvisorHelper()], ["us-east-1"]),
    ]
    for s3_key, services, target_regions in service_groups:
        ret = []
        for service in services:
            regions = session.get_available_regions(service.name) if target_regions is None else target_regions
            for region in regions:
                start, items = time(), []
                try:
                    items = service.process_request(session, region, account_id)
                    ret.extend(items)
                except ClientError as e:
                    if e.response["Error"]["Code"] in [
                        "AccessDenied", "AccessDeniedException", "AuthFailure", "InvalidClientTokenId",
                        "UnrecognizedClientException"
                    ]:
                        logging.warning(f"Unable to process {account_id} {service.name} in region {region}")
                    else:
                        raise
                finally:
                    logging.info(f"{service.name}: {account_id}, {region}, cnt={len(items)}, time={time() - start}s")
        for item in ret:
            logging.debug(item)
        write_to_s3(ret, s3_key)


if __name__ == "__main__":
    """Entry point for running from command line"""
    start = time()
    try:
        from configparser import ConfigParser
        from os.path import expanduser, join
        profile_names = []
        try:
            cp = ConfigParser()
            cp.read(join(expanduser("~"), ".aws", "credentials"))
            profile_names = cp.sections()
        except Exception as e:
            logging.error(e)
        accounts_processed = []
        for profile_name in profile_names:
            session = Session(profile_name=profile_name)
            account_id = session.client("sts").get_caller_identity()["Account"]
            if account_id in accounts_processed:
                continue
            accounts_processed.append(account_id)
            process_account(session, account_id)
    finally:
        logging.info(f"Lambda execution time: {time() - start}s")

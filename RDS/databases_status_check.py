from abc import ABC, abstractmethod
from boto3.session import Session
from botocore.exceptions import ClientError
import click
import logging
from time import time

# Update the root logger to get messages at DEBUG and above
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger("botocore").setLevel(logging.CRITICAL)
logging.getLogger("boto3").setLevel(logging.CRITICAL)
logging.getLogger("urllib3.connectionpool").setLevel(logging.CRITICAL)


def read_profile_names():
    from configparser import ConfigParser
    from os.path import expanduser, join
    try:
        cp = ConfigParser()
        cp.read(join(expanduser("~"), ".aws", "credentials"))
        return cp.sections()
    except Exception as e:
        logging.error(e)


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


class RdsHelper(Helper):
    """Neptune, DocumentDB info are also returned from rds.describe_db_instances."""
    def __init__(self):
        super().__init__("rds", "describe_db_instances")

    def process_response(self, item):
        if item.get("DBInstanceStatus") == "available":

            # Engine: aurora, aurora-mysql, aurora-postgresql, mariadb, oracle-*, postgres, sqlserver-*, neptune, docdb
            return {
                "Service": item["Engine"] if item["Engine"] in ["neptune", "docdb"] else "rds",
                "Engine": item["Engine"],
                "Id": item["DBInstanceIdentifier"],
                "BackupRetentionPeriod": item.get("BackupRetentionPeriod", 0),
                "MultiAZ": item["MultiAZ"],
                "EncryptedAtRest": item["StorageEncrypted"],
                "PublicFacing": item["PubliclyAccessible"],
            }


class ElastiCacheHelper(Helper):
    def __init__(self):
        super().__init__("elasticache", "describe_cache_clusters")

    def process_response(self, item):
        if item.get("CacheClusterStatus") == "available":
            return {
                "Service": self.name,
                "Engine": item["Engine"],    # memcached or redis
                "Id": item["CacheClusterId"],
                "BackupRetentionPeriod": item.get("SnapshotRetentionLimit", 0),
                "MultiAZ": item["PreferredAvailabilityZone"] == "Multiple",
                "EncryptedAtRest": item["AtRestEncryptionEnabled"],
            }


class RedshiftHelper(Helper):
    def __init__(self):
        super().__init__("redshift", "describe_clusters")

    def process_response(self, item):
        if item.get("ClusterAvailabilityStatus") != "Unavailable":
            return {
                "Service": self.name,
                "Engine": self.name,
                "Id": item.get("ClusterIdentifier"),
                "BackupRetentionPeriod": item.get("AutomatedSnapshotRetentionPeriod", 0),
                "MultiAZ": False,    # Redshift only supports Single-AZ deployments (last checked 2020-06-02)
                "EncryptedAtRest": item["Encrypted"],
                "PublicFacing": item["PubliclyAccessible"],

            }


class DynamoDBHelper(Helper):
    def __init__(self):
        super().__init__("dynamodb", "list_tables")

    def process_response(self, item):
        cb = self._client.describe_continuous_backups(TableName=item)    # item == table_name
        piir = cb["ContinuousBackupsDescription"]["PointInTimeRecoveryDescription"]["PointInTimeRecoveryStatus"] == "ENABLED"
        return {
            "Service": self.name,
            "Engine": self.name,
            "Id": item,
            "BackupRetentionPeriod": 35 if piir else 0,
            "MultiAZ": True,             # Always true
            "EncryptedAtRest": True,     # Always on
        }


def process_account(session, account_id, aws_region):
    for service in [RdsHelper(), DynamoDBHelper(), ElastiCacheHelper(), RedshiftHelper()]:
        regions = session.get_available_regions(service.name) if aws_region == "all" else [aws_region]
        ret = []
        for region in regions:
            start, items = time(), []
            try:
                items = service.process_request(session, region, account_id)
                ret.extend(items)
            except ClientError as e:
                if e.response["Error"]["Code"] in [
                    "AccessDenied", "AccessDeniedException", "AuthFailure", "UnrecognizedClientException"
                ]:
                    logging.warning(f"Unable to process {account_id} {service.name} in region {region}")
                else:
                    raise
            finally:
                logging.info(f"{service.name}: {account_id}, {region}, cnt={len(items)}, time={time() - start}s")

        for item in ret:
            logging.debug(item)


@click.command()
@click.option("--profile", "-p", help="AWS profile name")
@click.option("--region", "-r", help="AWS Region; use 'all' for all regions", default="ap-southeast-2")
def main(profile, region):
    start = time()
    try:
        accounts_processed = []
        profile_names = [profile] if profile else read_profile_names()
        for profile_name in profile_names:
            session = Session(profile_name=profile_name)
            account_id = session.client("sts").get_caller_identity()["Account"]
            if account_id in accounts_processed:
                continue
            accounts_processed.append(account_id)
            process_account(session, account_id, region)
    finally:
        logging.info(f"Lambda execution time: {time() - start}s")


if __name__ == "__main__": main()

"""
List databases status.
Supported: DocumentDB | DynamoDB | ElastiCache | MemoryDB | Neptune | RDS/Aurora | Redshift | Timestream | QLDB
TODO: Keyspaces

Output: [
    {
        "AccountId": in-string,
        "Region": in-string,
        "Service": docdb | dynamodb | elasticache | memorydb | neptune | rds | redshift | qldb
        "Engine": dynamodb | aurora | aurora-* | mariadb | oracle-* | postgres | sqlserver-* | neptune | docdb | memcached | redis | timestream | qldb
        "Id": in-string,
        "BackupRetentionPeriod": in-days,
        "MultiAZ": True | False,
        "EncryptedAtRest": True | False,
        "EncryptedInTransit": True | False,  # MemoryDB, QLDB
        "PubliclyAccessible": True | False,  # not available for Dynamodb, ElastiCache, MemoryDB
    },
]
"""
import logging
from abc import ABC, abstractmethod
from time import time

import click
from boto3.session import Session
from botocore.exceptions import ClientError

# Update the root logger to get messages at DEBUG and above
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger("botocore").setLevel(logging.CRITICAL)
logging.getLogger("boto3").setLevel(logging.CRITICAL)
logging.getLogger("urllib3.connectionpool").setLevel(logging.CRITICAL)


def read_aws_profile_names():
    from configparser import ConfigParser
    from os.path import expanduser, join
    try:
        cp = ConfigParser()
        cp.read(join(expanduser("~"), ".aws", "credentials"))
        return cp.sections()
    except Exception as e:
        logging.error(e)


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
        logging.info(f"Checking {self._name} {account_id} {region}")
        self._client = session.client(self.name, region_name=region)
        self._region, self._account_id = region, account_id
        ret = []
        for item in self.request_data():
            data = self.process_response(item)
            if data:
                data.update({"AccountId": account_id, "Region": region})
                ret.append(data)
        return ret

    def request_data(self):
        for page in self._client.get_paginator(self._request_func).paginate().result_key_iters():
            for item in page:
                if self._result_key is None:
                    yield item
                else:
                    for subitem in item[self._result_key]:
                        yield subitem

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

class MemoryDBHelper(Helper):
    def __init__(self):
        super().__init__("memorydb", "describe_clusters", result_key="Clusters")

    def process_response(self, item):
        if item.get("Status") == "available":
            return {
                "Service": self.name,
                "Engine": "redis",
                "Id": item.get("Name"),
                "BackupRetentionPeriod": item.get("SnapshotRetentionLimit", 0),
                "MultiAZ": item.get("AvailabilityMode", "singleaz") == "multiaz",
                "EncryptedAtRest": item.get("KmsKeyId") is not None,
                "EncryptedInTransit": item["TLSEnabled"],
            }

    def request_data(self):
        params = {}
        while True:
            resp = self._client.describe_clusters(**params)
            for item in resp[self._result_key]:
                yield item
            if resp.get("NextToken") is None:
                break
            params["NextToken"] = resp.get("NextToken")


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
                "PubliclyAccessible": item["PubliclyAccessible"],
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
                "PubliclyAccessible": item["PubliclyAccessible"],
            }


class TimestreamHelper(Helper):
    def __init__(self):
        super().__init__("timestream-write", "list_databases", result_key="Databases")

    def process_response(self, item):
        if item.get("State") == "ACTIVE":
            return {
                "Service": self.name,
                "Engine": self.name,
                "Id": item.get("DatabaseName"),
                "BackupRetentionPeriod": 0,
                "MultiAZ": True,  # Always true
                "EncryptedAtRest": True,
                "EncryptedInTransit": True,
            }

    def request_data(self):
        try:
            params = {}
            while True:
                resp = self._client.list_databases(**params)
                for item in resp[self._result_key]:
                    yield item
                if resp.get("NextToken") is None:
                    break
                params["NextToken"] = resp.get("NextToken")
        except Exception as e:
            logging.error(e)

class QLDBHelper(Helper):
    def __init__(self):
        super().__init__("qldb", "list_ledgers", result_key="Ledgers")

    def process_response(self, item):
        if item.get("State") == "ACTIVE":
            ledge = self._client.describe_ledger(Name=item["Name"])
            return {
                "Service": self.name,
                "Engine": self.name,
                "Id": ledge.get("Name"),
                "BackupRetentionPeriod": 0,
                "MultiAZ": True,  # Always true
                "EncryptedAtRest": ledge.get("EncryptionDescription", {}).get("EncryptionStatus") == "ENABLED",
                "EncryptedInTransit": True,
            }

    def request_data(self):
        params = {}
        while True:
            resp = self._client.list_ledgers(**params)
            for item in resp[self._result_key]:
                yield item
            if resp.get("NextToken") is None:
                break
            params["NextToken"] = resp.get("NextToken")


def process_account(session, account_id, aws_region):
    for service in [
        DynamoDBHelper(),
        ElastiCacheHelper(),
        MemoryDBHelper(),
        RdsHelper(),
        RedshiftHelper(),
        TimestreamHelper(),
        QLDBHelper(),
    ]:
        regions = session.get_available_regions(service.name) if aws_region == "all" else [aws_region]
        ret = []
        for region in regions:
            start, items = time(), []
            try:
                items = service.process_request(session, region, account_id)
                ret.extend(items)
            except ClientError as e:
                err_code = e.response["Error"]["Code"]
                if err_code in ["AccessDenied", "AccessDeniedException", "AuthFailure", "UnrecognizedClientException"]:
                    logging.warning(f"Unable to process {account_id} {service.name} in region {region}: {err_code}")
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
        profile_names = [profile] if profile else read_aws_profile_names()
        for profile_name in profile_names:
            session = Session(profile_name=profile_name)
            account_id = session.client("sts").get_caller_identity()["Account"]
            if account_id in accounts_processed:
                continue
            accounts_processed.append(account_id)
            process_account(session, account_id, region)
    finally:
        logging.info(f"Total execution time: {time() - start}s")


if __name__ == "__main__":
    main()

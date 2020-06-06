"""
Return tags of a supported service.
"""
from abc import ABC
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


def read_aws_profile_names():
    from configparser import ConfigParser
    from os.path import expanduser, join
    try:
        cp = ConfigParser()
        cp.read(join(expanduser("~"), ".aws", "credentials"))
        return cp.sections()
    except Exception as e:
        logging.error(e)


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
    def __init__(self, name, request_func, key_id_field, result_key=None, label=None):
        self._name = name
        self._key_id_field = key_id_field
        self._request_func = request_func
        self._result_key = result_key
        self._client = None
        self._region = None
        self._account_id = None
        self._label = label if label is not None else name
    
    @property
    def name(self):
        return self._name

    def get_tags(self, item):
        return item.get("Tags", [])

    def service_name(self, item):
        return item.get("Engine", self._label) if self._key_id_field is not None else self._label

    def process_response(self, item):
        return {
            "Service": self.service_name(item),
            "Id": item if self._key_id_field is None else item[self._key_id_field],
            "Tags": self.get_tags(item),
        }

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


class DynamoDBHelper(Helper):
    def __init__(self):
        super().__init__("dynamodb", "list_tables", key_id_field=None)

    def get_tags(self, item):
        return self._client.list_tags_of_resource(
            ResourceArn=f"arn:aws:dynamodb:{self._region}:{self._account_id}:table/{item}")["Tags"]


class EbsHelper(Helper):
    def __init__(self):
        super().__init__("ec2", "describe_volumes", "VolumeId", label="ebs")


class EC2Helpher(Helper):
    def __init__(self):
        super().__init__("ec2", "describe_instances", "InstanceId", "Instances")


class EfsHelper(Helper):
    def __init__(self):
        super().__init__("efs", "describe_file_systems", "FileSystemId")
    
    def get_tags(self, item):
        return self._client.describe_tags(FileSystemId=item["FileSystemId"])["Tags"]


class ElastiCacheHelper(Helper):
    def __init__(self):
        super().__init__("elasticache", "describe_cache_clusters", key_id_field="CacheClusterId")

    def get_tags(self, item):
        arn = item.get("ARN", f"arn:aws:elasticache:{self._region}:{self._account_id}:cluster:{item['CacheClusterId']}")
        return self._client.list_tags_for_resource(ResourceName=arn)["TagList"]


class ElbHelper(Helper):
    def __init__(self, v2=False):
        super().__init__("elbv2" if v2 else "elb", "describe_load_balancers", "LoadBalancerName")
    
    def get_tags(self, item):
        if self.name == "elb":
            return self._client.describe_tags(LoadBalancerNames=[item["LoadBalancerName"]])["TagDescriptions"][0][
                "Tags"]
        if self.name == "elbv2":
            return self._client.describe_tags(ResourceArns=[item["LoadBalancerArn"]])["TagDescriptions"][0]["Tags"]


class EsHelper(Helper):
    def __init__(self):
        super().__init__("es", None, "DomainName")
    
    def get_tags(self, item):
        return self._client.list_tags(ARN=item["ARN"])["TagList"]
    
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


class RdsHelper(Helper):
    """Neptune, DocumentDB information are also returned from rds.describe_db_instances."""
    def __init__(self):
        super().__init__("rds", "describe_db_instances", key_id_field="DBInstanceIdentifier")

    def get_tags(self, item):
        return self._client.list_tags_for_resource(ResourceName=item["DBInstanceArn"])["TagList"]

    def service_name(self, item=None):
        # Engine: aurora, aurora - mysql, aurora - postgresql, mariadb, oracle - *, postgres, sqlserver - *, neptune, docdb
        return item["Engine"] if ["Engine"] in ["neptune", "docdb", "aurora"] else "rds",


class RedshiftHelper(Helper):
    def __init__(self):
        super().__init__("redshift", "describe_clusters", key_id_field="ClusterIdentifier")


class S3Helper(Helper):
    def __init__(self):
        super().__init__("s3", "list_buckets", key_id_field=None)
    
    def get_tags(self, item):
        try:
            return self._client.get_bucket_tagging(Bucket=item).get("TagSet", [])
        except:
            return []
    
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



def process_account(session, account_id, service_name, aws_region):
    service = None
    if service_name in ["documentdb",  "neptune", "rds"]:   service = RdsHelper()
    elif service_name == "dynamodb":    service = DynamoDBHelper()
    elif service_name == "ec2":         service = EC2Helpher()
    elif service_name == "efs":         service = EfsHelper()
    elif service_name == "elasticache": service = ElastiCacheHelper()
    elif service_name == "elb":         service = ElbHelper()
    elif service_name == "es":          service = EsHelper()
    elif service_name == "redshift":    service = RedshiftHelper()
    elif service_name == "s3":          service = S3Helper()

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
@click.option("--service", "-s", required=True, type=click.Choice([
    "documentdb", "dynamodb", "ec2", "efs", "elasticache", "elb", "es", "neptune", "rds", "redshift", "s3",
], case_sensitive=False))
@click.option("--profile", "-p", help="AWS profile name")
@click.option("--region", "-r", help="AWS Region; use 'all' for all regions", default="ap-southeast-2")
def main(service, profile, region):
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
            process_account(session, account_id, service.lower(), region)
    finally:
        logging.info(f"Total execution time: {time() - start}s")


if __name__ == "__main__":
    main()

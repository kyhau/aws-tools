"""
Return tags of a supported service.
"""
from abc import ABC
import click
import logging
from arki_common.aws import AwsApiHelper

logging.getLogger().setLevel(logging.DEBUG)

SERVICES = ["documentdb", "dynamodb", "ec2", "efs", "elasticache", "elb", "es", "neptune", "rds", "redshift", "s3"]


class MainHelper(AwsApiHelper):
    def __init__(self, service_helper):
        super().__init__()
        self._service_helper = service_helper
        self._results = []

    def process_request(self, session, account_id, region, kwargs):
        items = self._service_helper.process_request(session, region, account_id,  kwargs.get("Key"))
        self._results.extend(items)
    
    def post_process(self):
        for item in self._results:
            logging.debug(item)


def get_tag_value(tags, key):
    for tag in tags:
        if tag["Key"].lower() == key.lower():
            return tag


def paginate(client, func_name, result_key=None):
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
        self._tag_key = None
    
    @property
    def name(self):
        return self._name

    def get_tags(self, item):
        return item.get("Tags", [])

    def service_name(self, item):
        return item.get("Engine", self._label) if self._key_id_field is not None else self._label

    def process_response(self, item):
        tags = self.get_tags(item)
        if tags and self._tag_key:
            tags = [get_tag_value(tags, self._tag_key)]
        
        if tags:
            return {
                "Service": self.service_name(item),
                "Id": item if self._key_id_field is None else item[self._key_id_field],
                "Tags": tags,
            }

    def process_request(self, session, region, account_id, tag_key):
        self._client = session.client(self.name, region_name=region)
        self._region, self._account_id = region, account_id
        self._tag_key = tag_key
        ret = []
        for item in paginate(self._client, self._request_func, self._result_key):
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
    
    def process_request(self, session, region, account_id, tag_key):
        self._client = session.client(self.name, region_name=region)
        self._region, self._account_id = region, account_id
        self._tag_key = tag_key
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
    
    def process_request(self, session, region, account_id, tag_key):
        self._client = session.client(self.name, region_name=region)
        self._region, self._account_id = region, account_id
        self._tag_key = tag_key
        ret = []
        for bucket_name in [x["Name"] for x in self._client.list_buckets()["Buckets"]]:
            data = self.process_response(bucket_name)
            if data:
                data.update({"AccountId": account_id, "Region": region})
                ret.append(data)
        return ret


@click.command()
@click.option("--service", "-s", required=True, type=click.Choice(SERVICES, case_sensitive=False))
@click.option("--tagkey", "-t", help="Tag key. Return all tags if not specified")
@click.option("--profile", "-p", help="AWS profile name. Use profiles in ~/.aws if not specified.")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS Region. Use 'all' for all regions.")
def main(service, tagkey, profile, region):
    service_name = service.lower()
    if service_name in ["documentdb", "neptune", "rds"]:
        helper = RdsHelper()
    elif service_name == "dynamodb":
        helper = DynamoDBHelper()
    elif service_name == "ec2":
        helper = EC2Helpher()
    elif service_name == "efs":
        helper = EfsHelper()
    elif service_name == "elasticache":
        helper = ElastiCacheHelper()
    elif service_name == "elb":
        helper = ElbHelper()
    elif service_name == "es":
        helper = EsHelper()
    elif service_name == "redshift":
        helper = RedshiftHelper()
    elif service_name == "s3":
        helper = S3Helper()
    else:
        helper = None
    
    MainHelper(helper).start(profile, region, helper.name, {"Key": tagkey})


if __name__ == "__main__":
    main()

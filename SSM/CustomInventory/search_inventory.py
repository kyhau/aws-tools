from boto3.session import Session
import botocore
import click
from configparser import ConfigParser
from datetime import datetime
import logging
from os.path import expanduser, join

# Update the root logger to get messages at DEBUG and above
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger("botocore").setLevel(logging.CRITICAL)
logging.getLogger("boto3").setLevel(logging.CRITICAL)
logging.getLogger("urllib3").setLevel(logging.CRITICAL)

# TODO Change inventory_type_name and processes below
# inventory_type_name = "Custom:Processes"
inventory_type_name = "Custom:DatabaseProcesses"
processes = ["sqlservr", "dse cassandra", "CassandraDaemon", "mysql", "postgres", "redis-server", "redis-sentinel", "memcached", "oninit"]

aws_profiles = []
try:
    cp = ConfigParser()
    cp.read(join(expanduser("~"), ".aws", "credentials"))
    aws_profiles = cp.sections()
except Exception as e:
    logging.error(e)


def get_instances_from_inventory(client):
    """
    Approach 1: retrieving ec2 instances from inventory.
    This approach will return data for all existing instances in record, including previous terminated instances.
    """
    ret = {}
    paginator = client.get_paginator("get_inventory")
    for page in paginator.paginate(
            Filters=[{"Key": "AWS:Service.Status", "Values": ["Running", "Stopped"], "Type":"Equal"}]):
        for item in page["Entities"]:
            try:
                for i in item["Data"]["AWS:InstanceInformation"]["Content"]:
                    ret[i["InstanceId"]] = [i["ComputerName"], i["IpAddress"]]
            except KeyError as e:
                pass
    return ret


def get_instances(ec2, instance_id=None):
    """Approach 2: retrieving current ec2 (running, stopping, stopped). Faster than approach 1.
    """
    def get_tag_value(tags, key="Name"):
        for tag in tags:
            if tag["Key"] == key:
                return tag["Value"]
        return ""
    data = lambda x: [get_tag_value(x.tags), x.private_ip_address]
    
    ret = {}
    if instance_id is None:
        for instance in ec2.instances.filter(
                Filters=[{"Name": "instance-state-name", "Values": ["running", "stopping", "stopped"]}]):
            ret[instance.id] = data(instance)
    else:
        for instance in ec2.instances.filter(InstanceIds=[instance_id]):
            ret[instance.id] = data(instance)
    return ret


def process_account(session, account_id, profile, aws_region, instanceid):
    regions = session.get_available_regions("ssm") if aws_region == "all" else [aws_region]
    for region in regions:
        logging.debug(f"Checking {account_id} {profile} {region}")
        try:
            ec2 = session.resource("ec2", region_name=region)
            instances = get_instances(ec2, instanceid)
            logging.debug(f"Number of instances to check: {len(instances)}")

            client = session.client("ssm", region_name=region)
            results = {}
            try:
                for instance_id in instances.keys():
                    resp = client.list_inventory_entries(InstanceId=instance_id, TypeName=inventory_type_name)
                    if resp["Entries"]:
                        for entry in resp["Entries"]:
                            for i in [x for x in processes if x in entry["Name"]]:
                                cap_time1 = datetime.strptime(resp["CaptureTime"], "%Y-%m-%dT%H:%M:%SZ")
                                cap_time0 = results.get((instance_id, i))
                                results[instance_id, i] = cap_time1 if cap_time0 is None else max(cap_time1, cap_time0)
            except botocore.errorfactory.ClientError as e:
                if e.response["Error"]["Code"] == "InvalidTypeNameException":
                    logging.warning(e)
                else:
                    raise
            except botocore.exceptions.ClientError as e:
                if e.response["Error"]["Code"] == "ThrottlingException":
                    logging.error(e)
                else:
                    raise
    
            for k in sorted(results.keys()):
                instance_id, key = k
                v = results[k]
                data = [
                    profile,
                    instance_id,
                    key,
                    instances[instance_id][0],    # ComputerName
                    instances[instance_id][1],    # IpAddress
                    str(v),
                ]
                print(",".join(data))

            if results and instanceid is not None:  # can stop searching
                return True
        
        except botocore.exceptions.ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code in ["AuthFailure", "UnrecognizedClientException"]:
                logging.warning(f"Unable to process region {region}: {error_code}")
            elif error_code == "InvalidInstanceID.NotFound":
                pass
            else:
                raise
        except Exception as e:
            logging.error(e)
            import traceback
            traceback.print_exc()


################################################################################
# Entry point

@click.command()
@click.option("--profile", "-p", help="AWS profile name")
@click.option("--instanceid", "-i", help="EC2 instance ID", default=None)
@click.option("--region", "-r", help="AWS Region; use 'all' for all regions", default="ap-southeast-2")
def main(profile, instanceid, region):
    accounts_processed = []
    profile_names = [profile] if profile else aws_profiles
    
    for profile_name in profile_names:
        try:
            session = Session(profile_name=profile_name)
            account_id = session.client("sts").get_caller_identity()["Account"]
            if account_id in accounts_processed:
                continue
            accounts_processed.append(account_id)
            
            if process_account(session, account_id, profile_name, region, instanceid) is not None:
                break
        
        except botocore.exceptions.ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code in ["ExpiredToken", "AccessDenied"]:
                logging.warning(f"{profile_name} {error_code}. Skipped")
            else:
                raise


if __name__ == "__main__": main()

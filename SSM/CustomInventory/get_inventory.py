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

inventory_type_name = "Custom:DatabaseProcesses"
processes = ["sqlservr", "cassandra", "dse", "mysql", "postgres", "redis", "memcached", "oninit"]

aws_profiles = []
try:
    cp = ConfigParser()
    cp.read(join(expanduser("~"), ".aws", "credentials"))
    aws_profiles = cp.sections()
except Exception as e:
    logging.error(e)

accounts_processed = []


def get_instances_from_inventory(client):
    ret = {}
    paginator = client.get_paginator("get_inventory")
    for page in paginator.paginate():
        for item in page["Entities"]:
            try:
                for i in item["Data"]["AWS:InstanceInformation"]["Content"]:
                    ret[i["InstanceId"]] = [i["ComputerName"], i["IpAddress"]]
            except KeyError as e:
                pass
    return ret


def list_action(session, instanceid, aws_region, profile):
    account_id = session.client("sts").get_caller_identity()["Account"]
    if account_id in accounts_processed:
        return
    accounts_processed.append(account_id)
    
    regions = session.get_available_regions("ssm") if aws_region == "all" else [aws_region]
    for region in regions:
        logging.debug(f"Checking {account_id} {profile} {region}")
        try:
            client = session.client("ssm", region_name=region)
            if instanceid is None:
                instances = get_instances_from_inventory(client)
            else:
                instances = {instanceid: [None, None]}

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
                    logging.error(e)
                else:
                    raise
    
            for k, v in results.items():
                instance_id, key = k
                data = [
                    profile,
                    instance_id,
                    instances[instance_id][0],    # ComputerName
                    instances[instance_id][1],    # IpAddress
                    key,
                    str(v),
                ]
                print(",".join(data))
        
        except botocore.exceptions.ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code in ["AuthFailure", "UnrecognizedClientException"]:
                logging.warning(f"Unable to process region {region}: {error_code}")
            elif error_code == "AccessDenied":
                logging.warning(f"Unable to process account {account_id}: {e}")
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
    profile_names = [profile] if profile else aws_profiles
    
    for profile_name in profile_names:
        try:
            session = Session(profile_name=profile_name)
            ret = list_action(session, instanceid, region, profile_name)
            if ret is not None:
                break
        
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "ExpiredToken":
                logging.warning(f"{profile_name} token expired. Skipped")
            else:
                raise


if __name__ == "__main__": main()

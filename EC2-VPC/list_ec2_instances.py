from boto3.session import Session
from botocore.exceptions import ClientError
import click
from configparser import ConfigParser
import logging
from os.path import expanduser, join

# Update the root logger to get messages at DEBUG and above
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger("botocore").setLevel(logging.CRITICAL)
logging.getLogger("boto3").setLevel(logging.CRITICAL)
logging.getLogger("urllib3").setLevel(logging.CRITICAL)

aws_profiles = []
try:
    cp = ConfigParser()
    cp.read(join(expanduser("~"), ".aws", "credentials"))
    aws_profiles = cp.sections()
except Exception as e:
    logging.error(e)

accounts_processed = []


def dump_data(response, account_id, region):
    for item in response["Reservations"]:
        for i in item["Instances"]:
            print(f"{account_id}, {region}, {i['InstanceId']}, {i.get('PrivateIpAddress')}, {i.get('PublicIpAddress')}")


def list_action(session, instanceid, aws_region):
    account_id = session.client("sts").get_caller_identity()["Account"]
    if account_id in accounts_processed:
        return
    accounts_processed.append(account_id)

    regions = session.get_available_regions("ec2") if aws_region is None else [aws_region]
    for region in regions:
        logging.debug(f"Checking {account_id} {region}")
        try:
            client = session.client("ec2", region_name=region)
            if instanceid is None:
                paginator = client.get_paginator("describe_instances")
                for page in paginator.paginate():
                    dump_data(page, account_id, region)
            else:
                ret = client.describe_instances(InstanceIds=[instanceid])
                dump_data(ret, account_id, region)
                return ret

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code in ["AuthFailure", "UnrecognizedClientException"]:
                logging.warning(f"Unable to process region {region}: {error_code}")
            elif error_code == "InvalidInstanceID.NotFound":
                pass
            else:
                raise
        except Exception as e:
            logging.error(e)


################################################################################
# Entry point

@click.command()
@click.option("--profile", "-p", help="AWS profile name")
@click.option("--instanceid", "-i", help="EC2 instance ID", default=None)
@click.option("--region", "-r", help="AWS Region", default=None)
def main(profile, instanceid, region):
    """
    Output: account_id, region, instance_id, private_ip, public_ip
    """
    profile_names = [profile] if profile else aws_profiles
    
    for profile_name in profile_names:
        try:
            session = Session(profile_name=profile_name)
            ret = list_action(session, instanceid, region)
            if ret is not None:
                break

        except ClientError as e:
            if e.response["Error"]["Code"] == "ExpiredToken":
                logging.warning(f"{profile_name} token expired. Skipped")
            else:
                raise

if __name__ == "__main__": main()

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
    for i in response["DBInstances"]:
        data = [
            account_id,
            region,
            i["DBInstanceIdentifier"],
            i["DBInstanceStatus"],
            i["Engine"],
            i["Endpoint"]["Address"],
            str(i["Endpoint"]["Port"]),
            "MultiAZ" if i["MultiAZ"] else "SingleAZ",
            i.get("CACertificateIdentifier", "None"),
        ]
        print(",".join(data))


def list_action(session, instanceid, aws_region):
    account_id = session.client("sts").get_caller_identity()["Account"]
    if account_id in accounts_processed:
        return
    accounts_processed.append(account_id)

    regions = session.get_available_regions("rds") if aws_region == "all" else [aws_region]
    for region in regions:
        logging.debug(f"Checking {account_id} {region}")
        try:
            client = session.client("rds", region_name=region)
            if instanceid is None:
                paginator = client.get_paginator("describe_db_instances")
                for page in paginator.paginate():
                    dump_data(page, account_id, region)
            else:
                ret = client.describe_db_instances(InstanceIds=[instanceid])
                dump_data(ret, account_id, region)
                return ret

        except ClientError as e:
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
            ret = list_action(session, instanceid, region)
            if ret is not None:
                break

        except ClientError as e:
            if e.response["Error"]["Code"] == "ExpiredToken":
                logging.warning(f"{profile_name} token expired. Skipped")
            else:
                raise

if __name__ == "__main__": main()

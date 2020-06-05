from boto3.session import Session
from botocore.exceptions import ClientError
import click
from configparser import ConfigParser
import logging
from os.path import expanduser, join

logging.getLogger().setLevel(logging.DEBUG)

aws_profiles = []
try:
    cp = ConfigParser()
    cp.read(join(expanduser("~"), ".aws", "credentials"))
    aws_profiles = cp.sections()
except Exception as e:
    logging.error(e)


def dump_data(response, account_id, region, profile):
    for i in response["DBInstances"]:
        data = [
            account_id,
            region,
            profile,
            i["DBInstanceIdentifier"],
            i["DBInstanceStatus"],
            i["Engine"],
            i["Endpoint"]["Address"],
            str(i["Endpoint"]["Port"]),
            "MultiAZ" if i["MultiAZ"] else "SingleAZ",
            i["PreferredMaintenanceWindow"],  # UTC
            i.get("CACertificateIdentifier", "None"),
        ]
        print(",".join(data))


def process_account(session, profile, account_id, aws_region, instance_id):
    regions = session.get_available_regions("rds") if aws_region == "all" else [aws_region]
    for region in regions:
        logging.debug(f"Checking {account_id} {region}")
        try:
            client = session.client("rds", region_name=region)
            if instance_id is None:
                paginator = client.get_paginator("describe_db_instances")
                for page in paginator.paginate():
                    dump_data(page, account_id, region, profile)
            else:
                ret = client.describe_db_instances(InstanceIds=[instance_id])
                dump_data(ret, account_id, region, profile)
                return ret

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code in ["AuthFailure", "UnrecognizedClientException"]:
                logging.warning(f"Unable to process region {region}: {error_code}")
            elif error_code == "InvalidInstanceID.NotFound":
                pass
            else:
                raise
        except Exception:
            import traceback
            traceback.print_exc()


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
            
            ret = process_account(session, profile_name, account_id, region, instanceid)
            if ret is not None:
                break
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code in ["ExpiredToken", "AccessDeniedException"]:
                logging.warning(f'{profile_name} {error_code}. Skipped')
            else:
                raise


if __name__ == "__main__": main()

"""
List RDS instances
Output: [
  [Account_id, Region, AWS-ProfileName, DBInstanceIdentifier, DBInstanceStatus, Engine, Endpoint-Address,
   Endpoint-Port, MultiAZ|SingleAZ, PreferredMaintenanceWindow(UTC), CACertificateIdentifier],
]
"""
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
            if error_code in ["AccessDenied", "AuthFailure", "UnrecognizedClientException"]:
                logging.warning(f"Unable to process region {region}: {error_code}")
            elif error_code == "InvalidInstanceID.NotFound":
                pass
            else:
                raise
        except Exception:
            import traceback
            traceback.print_exc()


@click.command()
@click.option("--instanceid", "-i", help="EC2 instance ID", default=None)
@click.option("--profile", "-p", help="AWS profile name")
@click.option("--region", "-r", help="AWS Region; use 'all' for all regions", default="ap-southeast-2")
def main(instanceid, profile, region):
    start = time()
    try:
        accounts_processed = []
        profile_names = [profile] if profile else read_aws_profile_names()
        for profile_name in profile_names:
            try:
                session = Session(profile_name=profile_name)
                account_id = session.client("sts").get_caller_identity()["Account"]
                if account_id in accounts_processed:
                    continue
                accounts_processed.append(account_id)

                if process_account(session, profile_name, account_id, region, instanceid) is not None:
                    break
            except ClientError as e:
                error_code = e.response["Error"]["Code"]
                if error_code in ["ExpiredToken", "InvalidClientTokenId"]:
                    logging.warning(f"{profile_name} {error_code}. Skipped")
                else:
                    raise
    finally:
        logging.info(f"Total execution time: {time() - start}s")


if __name__ == "__main__":
    main()

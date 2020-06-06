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

app_names = [
    "Microsoft SQL Server",  # MS SQL Server
    "sql",       # MMS SQL Server, MySQL Workbench, PostgreSQL
    "informix",  # IBM Informix
]


def read_aws_profile_names():
    from configparser import ConfigParser
    from os.path import expanduser, join
    try:
        cp = ConfigParser()
        cp.read(join(expanduser("~"), ".aws", "credentials"))
        return cp.sections()
    except Exception as e:
        logging.error(e)


def process_data(session, region, instance_id):
    client = session.client("ssm", region_name=region)
    resp = client.list_inventory_entries(InstanceId=instance_id, TypeName="AWS:Application")
    for entry in resp["Entries"]:
        matches = [ d for d in app_names if d in entry["Name"].lower() ]
        if matches:
            print(f"{instance_id}, {entry['Name']}")


def process_account(session, profile, aws_region, instance_id):
    regions = session.get_available_regions("ec2") if aws_region == "all" else [aws_region]
    for region in regions:
        logging.debug(f"Checking {profile} {region}")
        try:
            if instance_id:
                instance_ids = [instance_id]
            else:
                ec2 = session.resource("ec2", region_name=region)
                instance_ids = [instance.id for instance in ec2.instances.all()]

            for instance_id in instance_ids:
                process_data(session, region, instance_id)

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code in [
                "AccessDenied", "AuthFailure", "UnrecognizedClientException", "UnauthorizedOperation", "RequestExpired"
            ]:
                logging.warning(f"Unable to process region {region}: {error_code}")
            else:
                raise
        except Exception:
            import traceback
            traceback.print_exc()


@click.command()
@click.option("--instance", "-i", help="EC2 instance ID")
@click.option("--profile", "-p", help="AWS profile name")
@click.option("--region", "-r", help="AWS Region; use 'all' for all regions", default="ap-southeast-2")
def main(instance, profile, region):
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

                if process_account(session, profile_name, region, instance) is not None:
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

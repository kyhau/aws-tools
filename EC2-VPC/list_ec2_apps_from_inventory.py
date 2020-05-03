from boto3.session import Session
from botocore.exceptions import ClientError
import click
from configparser import ConfigParser
import logging
from os.path import expanduser, join

logging.getLogger().setLevel(logging.DEBUG)

app_names = [
    "Microsoft SQL Server",  # MS SQL Server
    "sql",       # MMS SQL Server, MySQL Workbench, PostgreSQL
    "informix",  # IBM Informix
]

aws_profiles = []
try:
    cp = ConfigParser()
    cp.read(join(expanduser("~"), ".aws", "credentials"))
    aws_profiles = cp.sections()
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
            if error_code in ["AuthFailure", "UnrecognizedClientException", "UnauthorizedOperation", "RequestExpired"]:
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
    accounts_processed = []
    profile_names = [profile] if profile else aws_profiles
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
            if error_code in ["ExpiredToken", "AccessDenied"]:
                logging.warning(f"{profile_name} {error_code}. Skipped")
            else:
                raise


if __name__ == "__main__": main()

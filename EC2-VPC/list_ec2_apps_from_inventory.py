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

accounts_processed = []


def process_data(instance_id, account_id, region, profile, session):
    client = session.client("ssm", region_name=region)
    resp = client.list_inventory_entries(InstanceId=instance_id, TypeName="AWS:Application")
    for entry in resp["Entries"]:
        matches = [ d for d in app_names if d in entry["Name"].lower() ]
        if matches:
            print(f"{instance_id}, {entry['Name']}")


def list_action(session, aws_region, profile, instance_id):
    account_id = session.client("sts").get_caller_identity()["Account"]
    if account_id in accounts_processed:
        return
    accounts_processed.append(account_id)

    regions = session.get_available_regions("ec2") if aws_region == "all" else [aws_region]
    for region in regions:
        logging.debug(f"Checking {account_id} {region}")
        try:
            if instance_id:
                instance_ids = [instance_id]
            else:
                ec2 = session.resource("ec2", region_name=region)
                instance_ids = [instance.id for instance in ec2.instances.all()]

            for instance_id in instance_ids:
                process_data(instance_id, account_id, region, profile, session)

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code in ["AuthFailure", "UnrecognizedClientException"]:
                logging.warning(f"Unable to process region {region}: {error_code}")
            elif error_code in ["AccessDenied", "UnauthorizedOperation", "RequestExpired"]:
                logging.warning(f"Unable to process account {account_id}: {e}")
            else:
                raise
        except Exception as e:
            logging.error(e)


################################################################################
# Entry point

@click.command()
@click.option("--profile", "-p", help="AWS profile name")
@click.option("--instance", "-i", help="EC2 instance ID")
@click.option("--region", "-r", help="AWS Region; use 'all' for all regions", default="ap-southeast-2")
def main(profile, instance, region):
    profile_names = [profile] if profile else aws_profiles
    
    for profile_name in profile_names:
        try:
            session = Session(profile_name=profile_name)
            ret = list_action(session, region, profile_name, instance)
            if ret is not None:
                break

        except ClientError as e:
            if e.response["Error"]["Code"] == "ExpiredToken":
                logging.warning(f"Profile [{profile_name}] token expired. Skipped")
            else:
                raise


if __name__ == "__main__": main()

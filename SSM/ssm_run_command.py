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

instance_ids = [
    
]
commands_to_run = [
    "tasklist | findstr sql"
]

aws_profiles = []
try:
    cp = ConfigParser()
    cp.read(join(expanduser("~"), ".aws", "credentials"))
    aws_profiles = cp.sections()
except Exception as e:
    logging.error(e)

accounts_processed = []


def do_something(session, instanceid, aws_region, profile):
    account_id = session.client("sts").get_caller_identity()["Account"]
    if account_id in accounts_processed:
        return
    accounts_processed.append(account_id)

    regions = session.get_available_regions("ssm") if aws_region == "all" else [aws_region]
    for region in regions:
        logging.debug(f"Checking {account_id} {region}")
        try:
            client = session.client("ssm", region_name=region)
            resp = client.send_command(
                InstanceIds=instance_ids,
                DocumentName="AWS-CheckIfSqlServerRunning",
                Parameters={
                    "commands": commands_to_run,
                }
            )
            command_id = resp["Command"]["CommandId"]
            logging.debug(command_id)
            
            for instance_id in instance_ids:
                output = client.get_command_invocation(
                    CommandId=command_id,
                    InstanceId=instance_id
                )
                print(output)

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
            ret = do_something(session, instanceid, region, profile_name)
            if ret is not None:
                break

        except ClientError as e:
            if e.response["Error"]["Code"] == "ExpiredToken":
                logging.warning(f"{profile_name} token expired. Skipped")
            else:
                raise


if __name__ == "__main__": main()

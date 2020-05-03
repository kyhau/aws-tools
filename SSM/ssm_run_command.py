from boto3.session import Session
from botocore.exceptions import ClientError
import click
from configparser import ConfigParser
import logging
from os.path import expanduser, join

logging.getLogger().setLevel(logging.DEBUG)

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


def do_something(session, profile, aws_region, instanceid):
    regions = session.get_available_regions("ssm") if aws_region == "all" else [aws_region]
    for region in regions:
        logging.debug(f"Checking {profile} {region}")
        try:
            client = session.client("ssm", region_name=region)
            resp = client.send_command(
                InstanceIds=instance_ids if instanceid is None else instanceid,
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
            
            if instanceid is not None:
                return instanceid

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


@click.command()
@click.option("--instanceid", "-i", help="EC2 instance ID", default=None)
@click.option("--profile", "-p", help="AWS profile name")
@click.option("--region", "-r", help="AWS Region; use 'all' for all regions", default="ap-southeast-2")
def main(instanceid, profile, region):
    accounts_processed = []
    profile_names = [profile] if profile else aws_profiles
    for profile_name in profile_names:
        try:
            session = Session(profile_name=profile_name)
            account_id = session.client("sts").get_caller_identity()["Account"]
            if account_id in accounts_processed:
                continue
            accounts_processed.append(account_id)
            
            if do_something(session, profile_name, region, instanceid) is not None:
                break
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code in ["ExpiredToken", "AccessDenied"]:
                logging.warning(f"{profile_name} {error_code}. Skipped")
            else:
                raise


if __name__ == "__main__": main()

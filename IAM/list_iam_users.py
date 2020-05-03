"""
List UserArn, CreateDate, PasswordLastUsed, AccessKeyMetadata
"""
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


def process_account(session):
    try:
        paginator = session.client("iam").get_paginator("list_users")
        for page in paginator.paginate():
            for user in page["Users"]:
                ret = session.client("iam").list_access_keys(UserName=user["UserName"])
                data = {
                    "Arn": user["Arn"],
                    "CreateData": user["CreateDate"],
                    "PasswordLastUsed": user.get("PasswordLastUsed"),
                    "AccessKeyMetadata": ret.get("AccessKeyMetadata"),
                }
                print(data)
    except Exception as e:
        logging.error(e)


@click.command()
@click.option("--profile", "-p", help="AWS profile name")
def main(profile):
    accounts_processed = []
    profile_names = [profile] if profile else aws_profiles
    for profile_name in profile_names:
        try:
            session = Session(profile_name=profile_name)
            account_id = session.client("sts").get_caller_identity()["Account"]
            if account_id in accounts_processed:
                continue
            accounts_processed.append(account_id)
            
            logging.debug(f"Checking {account_id} {profile}")
            process_account(session)
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code in ["ExpiredToken", "AccessDenied"]:
                logging.warning(f"{profile_name} {error_code}. Skipped")
            else:
                raise


if __name__ == "__main__": main()

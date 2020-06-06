"""
List UserArn, CreateDate, PasswordLastUsed, AccessKeyMetadata
"""
from boto3.session import Session
from botocore.exceptions import ClientError
import click
import logging
from time import time
import yaml

logging.getLogger().setLevel(logging.INFO)


def read_aws_profile_names():
    from configparser import ConfigParser
    from os.path import expanduser, join
    try:
        cp = ConfigParser()
        cp.read(join(expanduser("~"), ".aws", "credentials"))
        return cp.sections()
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
                print(yaml.dump(data, sort_keys=False))
    except Exception as e:
        logging.error(e)


@click.command()
@click.option("--profile", "-p", help="AWS profile name")
def main(profile):
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
                
                logging.debug(f"Checking {account_id} {profile}")
                process_account(session)
            except ClientError as e:
                error_code = e.response["Error"]["Code"]
                if error_code in ["ExpiredToken", "AccessDenied"]:
                    logging.warning(f"{profile_name} {error_code}. Skipped")
                else:
                    raise
    finally:
        logging.info(f"Total execution time: {time() - start}s")


if __name__ == "__main__":
    main()

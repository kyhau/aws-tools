"""
Print authorization details of User, Role, Group, LocalManagedPolicy, and/or AWSManagedPolicy in account(s).
"""
from boto3.session import Session
from botocore.exceptions import ClientError
import click
from configparser import ConfigParser
import logging
from os.path import expanduser, join
import yaml

logging.getLogger().setLevel(logging.DEBUG)

CHOICES = ["User", "Role", "Group", "LocalManagedPolicy", "AWSManagedPolicy"]

aws_profiles = []
try:
    cp = ConfigParser()
    cp.read(join(expanduser("~"), ".aws", "credentials"))
    aws_profiles = cp.sections()
except Exception as e:
    logging.error(e)


@click.command()
@click.option("--filter", "-f", type=click.Choice(CHOICES, case_sensitive=False))
@click.option("--profile", "-p", help="AWS profile name")
def main(filter, profile):
    operation_params = {"Filter": [filter]} if filter else {}
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

            paginator = session.client("iam").get_paginator("get_account_authorization_details")
            for page in paginator.paginate(**operation_params):
                for k, v in page.items():
                    if v and k not in ["ResponseMetadata", "IsTruncated"]:
                        print(yaml.dump(page[k]))

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code in ["ExpiredToken", "AccessDenied"]:
                logging.warning(f"{profile_name} {error_code}. Skipped")
            else:
                raise


if __name__ == "__main__": main()

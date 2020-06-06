"""
Print authorization details of User, Role, Group, LocalManagedPolicy, and/or AWSManagedPolicy in account(s).
"""
from boto3.session import Session
from botocore.exceptions import ClientError
import click
import logging
from time import time
import yaml

# Update the root logger to get messages at DEBUG and above
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger("botocore").setLevel(logging.CRITICAL)
logging.getLogger("boto3").setLevel(logging.CRITICAL)
logging.getLogger("urllib3.connectionpool").setLevel(logging.CRITICAL)

CHOICES = ["User", "Role", "Group", "LocalManagedPolicy", "AWSManagedPolicy"]


def read_aws_profile_names():
    from configparser import ConfigParser
    from os.path import expanduser, join
    try:
        cp = ConfigParser()
        cp.read(join(expanduser("~"), ".aws", "credentials"))
        return cp.sections()
    except Exception as e:
        logging.error(e)


@click.command()
@click.option("--filter", "-f", type=click.Choice(CHOICES, case_sensitive=False))
@click.option("--profile", "-p", help="AWS profile name")
def main(filter, profile):
    start = time()
    try:
        operation_params = {"Filter": [filter]} if filter else {}
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
    
                paginator = session.client("iam").get_paginator("get_account_authorization_details")
                for page in paginator.paginate(**operation_params):
                    for k, v in page.items():
                        if v and k not in ["ResponseMetadata", "IsTruncated"]:
                            print(yaml.dump(page[k]))
    
            except ClientError as e:
                error_code = e.response["Error"]["Code"]
                if error_code in ["AccessDenied", "ExpiredToken"]:
                    logging.warning(f"{profile_name} {error_code}. Skipped")
                else:
                    raise
    finally:
        logging.info(f"Total execution time: {time() - start}s")


if __name__ == "__main__":
    main()

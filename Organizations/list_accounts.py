"""
List account_id, alias, status

Output:
{
    account_id: {
        alias: string,
        status: string,
    },
}
"""
from boto3.session import Session
from botocore.exceptions import ClientError
import click
from collections import defaultdict
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


def process_account(session, account_id, results):
    try:
        # 1) Retrieve account id and alias at the (individual) account level. AWS supports only one alias per account
        aliases = session.client("iam").list_account_aliases()["AccountAliases"]
        results[account_id]["alias"] = aliases[0] if aliases else None
    except Exception as e:
        print(e)

    try:
        # 2) See if this session can access "list_accounts" from "organisation"
        paginator = session.client("organizations").get_paginator("list_accounts")
        for page in paginator.paginate():
            for acc in page["Accounts"]:
                results[acc["Id"]]["status"] = acc["Status"]
    except Exception as e:
        logging.error(e)


@click.command()
@click.option("--profile", "-p", help="AWS profile name")
def main(profile):
    start = time()
    try:
        accounts_processed = []
        profile_names = [profile] if profile else read_aws_profile_names()
        results = defaultdict(dict)
        for profile_name in profile_names:
            try:
                session = Session(profile_name=profile_name)
                account_id = session.client("sts").get_caller_identity()["Account"]
                if account_id in accounts_processed:
                    continue
                accounts_processed.append(account_id)
                
                process_account(session, account_id, results)
            except ClientError as e:
                error_code = e.response["Error"]["Code"]
                if error_code in ["ExpiredToken", "AccessDenied"]:
                    logging.warning(f"{profile_name} {error_code}. Skipped")
                else:
                    raise
    
        print("AccountId, Alias, Status")
        for account_id, data in results.items():
            print(f"{account_id}, {data['alias']}, {data['status']}")
    finally:
        logging.info(f"Total execution time: {time() - start}s")


if __name__ == "__main__":
    main()

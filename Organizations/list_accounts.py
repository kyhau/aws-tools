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
    accounts_processed = []
    profile_names = [profile] if profile else aws_profiles
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


if __name__ == "__main__": main()

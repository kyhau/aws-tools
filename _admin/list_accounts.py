"""
List account_id, alias, status
"""
from boto3.session import Session
import click
from collections import defaultdict

from arki_common.aws import assume_role, read_role_arns_from_file, DEFAULT_ROLE_ARNS_FILE
from arki_common.utils import print_json


def list_action(session, results):
    try:
        # 1) Retrieve account id and alias at the (individual) account level. AWS supports only one alias per account
        account_id = session.client("sts").get_caller_identity()["Account"]
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
        print(e)


################################################################################
# Entry point

@click.command()
@click.option("--profile", "-p", help="AWS profile name")
@click.option("--rolesfile", "-f", default=DEFAULT_ROLE_ARNS_FILE, help="Files containing Role ARNs")
def main(profile, rolesfile):
    results = defaultdict(dict)
    """ Example:
    {
        account_id: {
            alias: string,
            status: string,
        },
    }
    """

    if profile is not None:
        session = Session(profile_name=profile)
        list_action(session, results)

    for role_arn in read_role_arns_from_file(filename=rolesfile):
        session = assume_role(role_arn=role_arn)
        list_action(session, results)

    print("AccountId, Alias, Status")
    for account_id, data in results.items():
        print(f"{account_id}, {data['alias']}, {data['status']}")


if __name__ == "__main__": main()

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
from arki_common.aws import AwsApiHelper

logging.getLogger().setLevel(logging.DEBUG)


class Helper(AwsApiHelper):
    def __init__(self):
        super().__init__()
        self.results = defaultdict(dict)

    def process_request(self, session, account_id, region, kwargs):
        try:
            # 1) Retrieve account id and alias at the (individual) account level. AWS supports only one alias per account
            aliases = session.client("iam").list_account_aliases()["AccountAliases"]
            self.results[account_id]["alias"] = aliases[0] if aliases else None
        except Exception as e:
            print(e)
    
        try:
            # 2) See if this session can access "list_accounts" from "organisation"
            paginator = session.client("organizations").get_paginator("list_accounts")
            for page in paginator.paginate():
                for acc in page["Accounts"]:
                    self.results[acc["Id"]]["status"] = acc["Status"]
        except Exception as e:
            logging.error(e)
    
    def post_process(self):
        if self.results:
            print("AccountId, Alias, Status")
            for account_id, data in self.results.items():
                print(f"{account_id}, {data.get('alias')}, {data.get('status')}")


@click.command()
@click.option("--profile", "-p", help="AWS profile name. Use profiles in ~/.aws if not specified.")
def main(profile):
    Helper().start(profile, "ap-southeast-2", "iam")


if __name__ == "__main__":
    main()

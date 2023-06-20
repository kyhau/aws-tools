#!/usr/bin/env python
import json

import click
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SOURCE = "https://raw.githubusercontent.com/rupertbg/aws-public-account-ids/master/accounts.json"


@click.command(help="Get public AWS account IDs")
@click.option("--account", "-a", help="Account ID to search")
@click.option("--keyword", "-k", help="Keyword to search")
def main(account, keyword):
    items = requests.get(SOURCE, verify=False).json()

    result = items
    if account:
        result = [item for item in items if item["id"] == account]
    if keyword:
        keyword = keyword.lower()
        result = [item for item in items if keyword in json.dumps(item).lower()]

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
     main()

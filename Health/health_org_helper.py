"""
Export affected resources of an AWS Health event for accounts in an organization.
- Prerequisites: pip install boto3 click
- Filter: Return only affected resources with status other than "RESOLVED"
- Input file: see sample_accounts.json for input example.
- Output file: health_org_helper.json
"""
import json
import logging

import boto3
import click
from botocore.exceptions import ClientError

OUTPUT_FILE = "health_org_helper.json"
NOT_FILTERS = ["RESOLVED"]


def write_json_file(filename, data, indent=0, sort_keys=True):
    with open(filename, "w") as f:
        return json.dump(data, f, default=str, indent=indent, sort_keys=sort_keys)


def accounts(filename):
    with open(filename) as f:
        ret = json.load(f)
        accounts = {
            account["AccountNumber"]: account["AccountName"] for account in ret \
                if account["Type"] == "Internal" and account["Status"] == "Active"
        }
        return accounts


def process_account(health_client, eventArn, account_id):
    ret = []
    try:
        params = {
            "organizationEntityFilters": [{
                "eventArn": eventArn,
                "awsAccountId": account_id
            }]
        }

        for page in health_client.get_paginator("describe_affected_entities_for_organization").paginate(**params):
            if page.get("failedSet"):
                raise Exception("failedSet: {}".format(page["failedSet"]))

            for item in page["entities"]:
                if item["statusCode"] not in NOT_FILTERS:
                    ret.append(item)

    except ClientError as e:
        logging.error(e)

    return ret


def process(health_client, eventArn, accounts):
    result_set = {}
    for account_id, account_alias in accounts.items():
        ret = process_account(health_client, eventArn, account_id)
        if ret:
            result_set[account_alias] = ret
    return result_set


@click.command()
@click.option("--accounts-file", "-f", required=True, help="JSON file containing account IDs and names")
@click.option("--event-arn", "-e", required=True, help="AWS Health event ARN")
@click.option("--profile", "-p", default="default", help="AWS profile name. Use default if not specified")
def main(accounts_file, event_arn, profile):
    health_client = boto3.session.Session(profile_name=profile).client("health", region_name="us-east-1")
    ret = process(health_client, eventArn=event_arn, accounts=accounts(accounts_file))
    write_json_file(OUTPUT_FILE, ret, indent=2, sort_keys=True)


if __name__ == "__main__":
    main()

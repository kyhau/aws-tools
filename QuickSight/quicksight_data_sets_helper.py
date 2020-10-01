"""
A simple script supports adding owner permissions to a set of data sets.
"""
import json
import logging

import click
from boto3.session import Session

logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger("botocore").setLevel(logging.CRITICAL)
logging.getLogger("boto3").setLevel(logging.CRITICAL)
logging.getLogger("urllib3.connectionpool").setLevel(logging.CRITICAL)

new_permission = {
    "Principal": None,
    "Actions": [
        "quicksight:CancelIngestion",
        "quicksight:CreateIngestion",
        "quicksight:DeleteDataSet",
        "quicksight:DescribeDataSet",
        "quicksight:DescribeDataSetPermissions",
        "quicksight:DescribeIngestion",
        "quicksight:ListIngestions",
        "quicksight:PassDataSet",
        "quicksight:UpdateDataSet",
        "quicksight:UpdateDataSetPermissions",
    ]
}

def dump_output(ret, filename):
    with open(filename, "w") as f:
        json.dump(ret, f, indent=2, sort_keys=True)

    print(json.dumps(ret, indent=2, sort_keys=True))


@click.group(invoke_without_command=False, help="QuickSight Helper")
@click.option("--profile", "-p", default="default", show_default=True, help="AWS profile name")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS Region")
@click.pass_context
def main_cli(ctx, profile, region):
    session = Session(profile_name=profile)
    ctx.obj = {
        "client": session.client("quicksight", region_name=region),
        "account": session.client("sts").get_caller_identity()["Account"],
    }


@main_cli.command(help="Output all data set names and IDs to console and file")
@click.option("--keyword", "-k", help="Keyword in names")
@click.pass_context
def ls(ctx, keyword):
    client = ctx.obj["client"]
    account_id = ctx.obj["account"]

    next_token, ret = None, {}
    while True:
        params = {"AwsAccountId": account_id}
        if next_token:
            params["NextToken"] = next_token

        resp = client.list_data_sets(**params)
        for r in resp["DataSetSummaries"]:
            if keyword is None or keyword.lower() in r["Name"].lower():
                ret[r["DataSetId"]] = r["Name"]

        next_token = resp.get("NextToken")
        if next_token is None:
            break

    dump_output(ret, "quicksight_data_set_ids.json")
    logging.info(f"Total num of Data Sets: {len(ret)}")


@main_cli.command(help="Output all Data Set permissions to console and file")
@click.option("--id-file", "-i", default="quicksight_data_set_ids.json", show_default=True)
@click.pass_context
def permissions(ctx, id_file):
    client = ctx.obj["client"]
    account_id = ctx.obj["account"]

    with open(id_file, "r") as f:
        data_set_ids = json.load(f)

    ret = {}
    for id, name in data_set_ids.items():
        ret[id] = {
            "Name": name,
            "Permissions": client.describe_data_set_permissions(AwsAccountId=account_id, DataSetId=id)["Permissions"]
        }

    dump_output(ret, "quicksight_data_set_permissions.json")


@main_cli.command(help="Add owner permissions to the Data Sets in the input file")
@click.argument("user_arn", type=click.STRING)
@click.option("--id-file", "-i", default="quicksight_data_set_ids.json", show_default=True)
@click.pass_context
def add_owner_permissions(ctx, user_arn, id_file):
    client = ctx.obj["client"]
    account_id = ctx.obj["account"]

    with open(id_file, "r") as f:
        data_set_ids = json.load(f)

    new_permission["Principal"] = user_arn

    for name, id in data_set_ids.items():
        print(name)
        resp = client.update_data_set_permissions(AwsAccountId=account_id,DataSetId=id,GrantPermissions=[new_permission])
        print(json.dumps(resp, indent=2, sort_keys=True))


if __name__ == "__main__":
    main_cli(obj={"debug": "true"})

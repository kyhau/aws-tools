from boto3.session import Session
from boto3.dynamodb.conditions import Attr
import click
import datetime
import decimal
import json
import logging
from time import mktime

logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger("botocore").setLevel(logging.CRITICAL)
logging.getLogger("boto3").setLevel(logging.CRITICAL)
logging.getLogger("urllib3.connectionpool").setLevel(logging.CRITICAL)


class DecimalEncoder(json.JSONEncoder):
    """Helper class to convert a DynamoDB item to JSON."""
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


class DefaultEncoder(json.JSONEncoder):
    """Encode for the json."""
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return int(mktime(obj.timetuple()))
        return json.JSONEncoder.default(self, obj)


dump_json = lambda x: json.dumps(x, cls=DefaultEncoder, sort_keys=True, indent=2)


def list_items_with_pagination(client, table_name, field_name=None, field_value=None):
    """
    Scan and return all items with paginator
    Note that this approach will return low level data
    See https://stackoverflow.com/questions/36780856/complete-scan-of-dynamodb-with-boto3
    """
    paginator = client.get_paginator("scan")
    operation_params = {"TableName": table_name,}
    if field_name and field_value:
        operation_params.update({
            "FilterExpression": f"{field_name} = :x",
            "ExpressionAttributeValues": {
                ":x": {"S": field_value}
            }
        })
    for page in paginator.paginate(**operation_params):
        yield page["Items"]


@click.group(help="Simple DynamoDB helper")
@click.option("--profile", "-p", default="default", help="AWS profile name")
@click.option("--region", "-r", default="ap-southeast-2", help="AWS region")
@click.pass_context
def cli_main(ctx, profile, region):
    session = Session(profile_name=profile)
    ctx.obj = {"session": session, "region": region}
    # TODO support local ddb dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")


@cli_main.command(help="Print all DynamoDB tables")
@click.pass_context
def list(ctx):
    ddb_client = ctx.obj["session"].client("dynamodb", ctx.obj["region"])
    for page in ddb_client.get_paginator("list_tables").paginate().result_key_iters():
        for item in page:
            print(item)


@cli_main.command(help="Describe table")
@click.argument("table_name", required=True)
@click.pass_context
def describe(ctx, table_name):
    ddb_client = ctx.obj["session"].client("dynamodb", ctx.obj["region"])
    table_info = ddb_client.describe_table(TableName=table_name)["Table"]
    print(dump_json(table_info))


@cli_main.command(help="Scan table")
@click.argument("table_name", required=True)
@click.option("--field-name", "-k", help="Field name")
@click.option("--field-value", "-v", help="Field value")
@click.pass_context
def scan(ctx, table_name, field_name, field_value):
    table = ctx.obj["session"].resource("dynamodb", ctx.obj["region"]).Table(table_name)

    params = {}
    if field_name and field_value:
        params["FilterExpression"] = Attr(field_name).eq(field_value)

    resp = table.scan(**params)
    for item in resp["Items"]:
        print(item)
    
    while "LastEvaluatedKey" in resp:
        params.update({"ExclusiveStartKey": resp["LastEvaluatedKey"]})
        resp = table.scan(**params)
        for item in resp["Items"]:
            print(item)


if __name__ == "__main__":
    cli_main(obj={})

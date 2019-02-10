import boto3
from boto3.dynamodb.conditions import Attr
import click
import decimal
import json
import logging
from os.path import basename
from arki.aws import print_json
from arki.configs import (
    init_wrapper,
    default_config_file_path,
)


APP_NAME = basename(__file__).split('.')[0]

# Default configuration file location
DEFAULT_CONFIG_FILE = default_config_file_path(f"{APP_NAME}.toml")

DEFAULT_CONFIGS = {
    "aws.profile": {"required": True},
}


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


def list_ddb_tables(client):
    paginator = client.get_paginator("list_tables")

    # Limit is 100
    tables = []
    for page in paginator.paginate():
        tables.extend(page["TableNames"])
    return tables


def describe_ddb_table(client, table_name):
    return client.describe_table(TableName=table_name)["Table"]


def list_items_with_pagination(client, table_name, field_name=None, field_value=None):
    """Scan and return all items
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


def scan_ddb_table(table, field_name=None, field_value=None):
    """Scan and return all items
    """
    if field_value and field_value:
        resp = table.scan(FilterExpression=Attr(field_name).eq(field_value))
        items = resp["Items"]
        while "LastEvaluatedKey" in resp:
            resp = table.scan(
                FilterExpression=Attr(field_name).eq(field_value),
                ExclusiveStartKey=resp["LastEvaluatedKey"]
            )
            items.extend(resp["Items"])
    else:
        resp = table.scan()
        items = resp["Items"]
        while "LastEvaluatedKey" in resp:
            resp = table.scan(ExclusiveStartKey=resp["LastEvaluatedKey"])
            items.extend(resp["Items"])
    return items


def delete_items(client, table_name, field_name, field_value):
    keys = describe_ddb_table(client, table_name=table_name)["KeySchema"]
    key1 = keys[0]["AttributeName"]

    table = boto3.resource("dynamodb").Table(table_name)

    for item in scan_ddb_table(table, field_name, field_value):
        logging.debug(f"Deleting item with key({key1}): {item[key1]}...")
        table.delete_item(Key={key1: item[key1]})


@init_wrapper
def process(*args, **kwargs):
    try:
        config_file = kwargs.get("config_file")
        configs = kwargs.get("_arki_configs")
        settings = kwargs.get("_arki_settings")
        list_tables = kwargs.get("list_tables")
        describe_table = kwargs.get("describe_table")
        scan_table = kwargs.get("scan_table")

        client = boto3.client("dynamodb")

        if list_tables:
            tables = list_ddb_tables(client)
            cnt = 1
            for table_name in tables:
                print(f"{cnt}: {table_name}")
                cnt += 1

        elif describe_table:
            table_info = describe_ddb_table(client, table_name=describe_table)
            print_json(table_info)

        elif scan_table:
            table = boto3.resource("dynamodb").Table(scan_table)
            for item in scan_ddb_table(table):
                print(item)

        else:
            print(f"Profiles in {config_file}\n-------------------------")
            for s in configs.keys():
                print(s)

    except Exception as e:
        logging.error(e)
        return 1

    return 0


@click.command()
@click.argument("config_file", required=False, default=DEFAULT_CONFIG_FILE)
@click.option("--config_section", "-s", required=False, default=APP_NAME, help=f"E.g. {APP_NAME}.staging")
@click.option("--list_tables", "-l", is_flag=True, help="Return all records of the given table name")
@click.option("--describe_table", "-d", help="Describe the table of the given table name")
@click.option("--scan_table", "-s", help="Return all records of the given table name")
def main(config_file, config_section, list_tables, describe_table, scan_table):
    """
    aws_ddb prints all profiles (sections) defined in the toml file, if any.

    Use --list_tables to print all DynamoDB Tables that the given credentials have accessed to.

    Use --describe_table TABLE_NAME to describe the given table (e.g. number of items etc.).

    Use --scan_table TABLE_NAME to return all records of the given table name.

    Use --init to create a `ini_file` with the default template to start.
    """

    process(
        app_name=APP_NAME,
        config_file=config_file,
        default_configs=DEFAULT_CONFIGS,
        config_section=config_section,
        list_tables=list_tables,
        describe_table=describe_table,
        scan_table=scan_table,
    )

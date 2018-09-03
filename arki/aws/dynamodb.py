import boto3
from boto3.dynamodb.conditions import Attr
import click
import decimal
import json
import logging
from os.path import join
import sys
from arki.aws import print_json
from arki.configs import ARKI_LOCAL_STORE_ROOT, create_ini_template, read_configs, get_configs_sections
from arki import init_logging


# Default configuration file location
ENV_STORE_FILE = join(ARKI_LOCAL_STORE_ROOT, "ddb.ini")

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


@click.command()
@click.argument("ini_file", required=False, default=ENV_STORE_FILE)
@click.option("--init", "-i", is_flag=True, help="Set up new configuration")
@click.option("--profile", "-p", help="The profile (section) to be used in the .ini file")
@click.option("--list_tables", "-l", is_flag=True, help="Return all records of the given table name")
@click.option("--describe_table", "-d", help="Describe the table of the given table name")
@click.option("--scan_table", "-s", help="Return all records of the given table name")
def main(ini_file, init, profile, list_tables, describe_table, scan_table):
    """
    aws_ddb prints all profiles (sections) defined in the .ini file, if any.

    Use --list_tables to print all DynamoDB Tables that the given credentials have accessed to.

    Use --describe_table TABLE_NAME to describe the given table (e.g. number of items etc.).

    Use --scan_table TABLE_NAME to return all records of the given table name.

    Use --init to create a `ini_file` with the default template to start.
    """

    try:
        init_logging()

        if init:
            create_ini_template(
                ini_file=ini_file,
                module=__file__,
                config_dict=DEFAULT_CONFIGS,
                allow_overriding_default=True
            )

        else:
            settings = read_configs(
                ini_file=ini_file,
                config_dict=DEFAULT_CONFIGS,
                section_list=[profile] if profile else None
            )
            boto3.setup_default_session(profile_name=settings["aws.profile"])
            client = boto3.client("dynamodb")

            if list_tables:
                tables = list_ddb_tables(client)
                cnt = 1
                for table_name in tables:
                    print(f"{cnt}: {table_name}")
                    cnt+=1

            elif describe_table:
                table_info = describe_ddb_table(client, table_name=describe_table)
                print_json(table_info)

            elif scan_table:
                table = boto3.resource("dynamodb").Table(scan_table)
                for item in scan_ddb_table(table):
                    print(item)

            else:
                print(f"Profiles in {ENV_STORE_FILE}\n-------------------------")
                sections = get_configs_sections(ini_file)
                for s in sections:
                    print(s)

    except Exception as e:
        logging.error(e)
        sys.exit(1)

    sys.exit(0)
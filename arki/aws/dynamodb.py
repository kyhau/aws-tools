import boto3
from boto3.dynamodb.conditions import Key, Attr
import click
import decimal
import json
import logging
import sys
from arki.aws import check_response, print_json
from arki.configs import create_ini_template, read_configs
from arki import init_logging


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


def list_tables(aws_profile):
    #paginator = client.get_paginator("list_tables")

    client = boto3.Session(profile_name=aws_profile).client("dynamodb")
    resp = client.list_tables()

    if check_response(resp):
        cnt = 1
        for table_name in resp["TableNames"]:
            print(f"{cnt}: {table_name}")
            cnt+=1
        print("-------------------------")


def describe_table(aws_profile, table_name):
    return boto3.Session(profile_name=aws_profile).client("dynamodb").describe_table(TableName=table_name)["Table"]


def list_items_with_pagination(aws_profile, table_name, field_name=None, field_value=None):
    """Scan and return all items
    """
    paginator = boto3.Session(profile_name=aws_profile).client("dynamodb").get_paginator("scan")

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


def scan_table(aws_profile, table_name, field_name=None, field_value=None):
    """Scan and return all items
    """
    table = boto3.Session(profile_name=aws_profile).resource("dynamodb").Table(table_name)

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


def delete_items(aws_profile, table_name, field_name, field_value):
    keys = describe_table(aws_profile=aws_profile, table_name=table_name)["KeySchema"]
    key1 = keys[0]["AttributeName"]

    table = boto3.Session(profile_name=aws_profile).resource("dynamodb").Table(table_name)

    for item in scan_table(aws_profile, table_name, field_name, field_value):
        logging.debug(f"Deleting item with key({key1}): {item[key1]}...")
        table.delete_item(Key={key1: item[key1]})


@click.command()
@click.argument("ini_file", required=False)
@click.option("--init", "-i", is_flag=True, help="Set up new configuration")
@click.option("--table", "-t", help="Table name")
@click.option("--scan", "-s", is_flag=True, help="Set up new configuration")
def main(ini_file, init, table, scan):
    """
    Reimport the API Swagger template to AWS.

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
            profile_name=None
            if ini_file:
                settings = read_configs(ini_file=ini_file, config_dict=DEFAULT_CONFIGS)
                profile_name = settings["aws.profile"]

            if table:
                if scan:
                    for item in scan_table(
                        aws_profile=profile_name,
                        table_name=table,
                    ):
                        print(item)
                else:
                    table_info = describe_table(aws_profile=profile_name, table_name=table)
                    print_json(table_info)

            else:
                list_tables(aws_profile=profile_name)


    except Exception as e:
        logging.error(e)
        sys.exit(1)

    sys.exit(0)
"""
Delete items from a table
"""
import boto3
from boto3.dynamodb.conditions import Attr
import click
import logging
from time import time

logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger("botocore").setLevel(logging.CRITICAL)
logging.getLogger("boto3").setLevel(logging.CRITICAL)
logging.getLogger("urllib3.connectionpool").setLevel(logging.CRITICAL)


@click.command(help="Delete items from a table")
@click.argument("table_name", required=True)
@click.option("--field-name", "-f", help="Field name")
@click.option("--field-value", "-v", help="Field value")
@click.option("--key-field-name", "-k", required=True, help="Key field name")
def main(table_name, field_name, field_value, key_field_name):
    start = time()

    table = boto3.resource("dynamodb").Table(table_name)

    params = {"ProjectionExpression": key_field_name}
    if field_name and field_value:
        params["FilterExpression"] = Attr(field_name).eq(field_value)

    resp = None
    with table.batch_writer() as batch:
        count = 0
        while resp is None or "LastEvaluatedKey" in resp:
            if resp is not None and "LastEvaluatedKey" in resp:
                params.update({"ExclusiveStartKey": resp["LastEvaluatedKey"]})

            resp = table.scan(**params)
            for item in resp["Items"]:
                logging.debug(f"{count}: {item}")
                batch.delete_item(Key={key_field_name: item[key_field_name]})
                count += 1

    logging.info(f"Total execution time: {time() - start}s")


if __name__ == "__main__":
    main()

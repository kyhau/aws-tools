import csv
import logging
import time

import boto3
import click

logging.getLogger().setLevel(logging.INFO)
logging.getLogger("botocore").setLevel(logging.CRITICAL)
logging.getLogger("boto3").setLevel(logging.CRITICAL)

client = boto3.client("cloudformation")


def get_account_region_list_from_input_file(input_csv_file):
    account_region_list = []

    with open(input_csv_file, "r") as f:
        lines = [list(map(str.strip, line)) for line in csv.reader(f, delimiter=',')]
        for line in lines:
            account_region_list.append((line[0], line[1]))  # account_id, region
    return account_region_list


def get_current_stack_instances(stack_set_name):
    account_region_list = []
    for page in client.get_paginator("list_stack_instances").paginate(StackSetName=stack_set_name).result_key_iters():
        for item in page:
            account_region_list.append((item["Account"], item["Region"]))
    return account_region_list


def create_stack_set_instance(stack_set_name, account_id, region_name):
    resp = client.create_stack_instances(StackSetName=stack_set_name, Accounts=[account_id], Regions=[region_name])
    operation_id = resp["OperationId"]

    cnt, status = 0, None
    while cnt < 100 and status not in ["SUCCEEDED", "FAILED", "STOPPED"]:
        cnt += 1
        time.sleep(6)
        resp = client.describe_stack_set_operation(StackSetName=stack_set_name, OperationId=operation_id)
        status = resp["StackSetOperation"]["Status"]  # 'Status': 'RUNNING'|'SUCCEEDED'|'FAILED'|'STOPPING'|'STOPPED'|'QUEUED'
        logging.info(f"CheckPt {cnt}: operation_id={operation_id} status={status}")

    if status != "SUCCEEDED":
        raise Exception(f"Unexpected status ({status}) on create_stack_set_instance {stack_set_name} {account_id} {region_name} operation_id={operation_id}")


@click.command(help="Manage Stack Set Instances")
@click.option("--dry-run", "-d", is_flag=True, show_default=True, help="Dry run, no functional change.")
@click.option("--input-file", "-f", required=True, help="Path to input csv file containing account_id,region per line.")
@click.option("--stack-set-name", "-n", required=True, help="Stack Set Name.")
def main(dry_run, input_file, stack_set_name):
    input_account_region_list = get_account_region_list_from_input_file(input_file)
    curr_account_region_list = get_current_stack_instances(stack_set_name)

    cnt_add = 0
    for input_item in input_account_region_list:
        if input_item not in curr_account_region_list:
            cnt_add += 1
            account_id, region_name = input_item

            logging.info(f"Adding new stack set instance for {stack_set_name} in {account_id} {region_name}")

            if dry_run is False:
                create_stack_set_instance(stack_set_name, account_id, region_name)

    logging.info(f"Total num of new stack set instances: {cnt_add}")


if __name__ == "__main__":
    main()

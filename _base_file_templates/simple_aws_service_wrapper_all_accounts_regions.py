"""
A simple helper function to ...
"""
from boto3.session import Session
from botocore.exceptions import ClientError
import click
import logging
from time import time

# Update the root logger to get messages at DEBUG and above
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger("botocore").setLevel(logging.CRITICAL)
logging.getLogger("boto3").setLevel(logging.CRITICAL)
logging.getLogger("urllib3.connectionpool").setLevel(logging.CRITICAL)


def read_aws_profile_names():
    from configparser import ConfigParser
    from os.path import expanduser, join
    try:
        cp = ConfigParser()
        cp.read(join(expanduser("~"), ".aws", "credentials"))
        return cp.sections()
    except Exception as e:
        logging.error(e)


def process_region(client, operation_params):
    cnt = 0
    for page in client.get_paginator("describe_subnets").paginate(**operation_params):
        for item in page["Subnets"]:
            mask = int(item["CidrBlock"].split("/")[1])
            usable_ip_cnt = 2 ** (32 - mask) - 5
            available_ip_cnt = item["AvailableIpAddressCount"]
            data = [
                f"{item['SubnetId']}: {item['CidrBlock']}",
                f"usable={usable_ip_cnt}",
                f"used={usable_ip_cnt - available_ip_cnt}",
                f"available={available_ip_cnt}",
            ]
            print(", ".join(data))
            cnt += 1
    return cnt


def process_account(session, profile, account_id, aws_region, subnet_id):
    operation_params = {"SubnetIds": [subnet_id]} if subnet_id else {}

    for region in session.get_available_regions("ec2") if aws_region == "all" else [aws_region]:
        logging.debug(f"Checking {account_id} {profile} {region}")
        try:
            client = session.client("ec2", region_name=region)
            cnt = process_region(client, operation_params)
            if cnt and subnet_id:
                return cnt

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code in ["AccessDenied", "AuthFailure", "UnrecognizedClientException"]:
                logging.warning(f"Unable to process region {region}: {error_code}")
            else:
                raise
        except Exception:
            import traceback
            traceback.print_exc()


@click.group(invoke_without_command=True, help="TODO help 1")
@click.option("--subnetid", "-s", help="Subnet ID, or show all if not specified.", default=None, show_default=True)
@click.option("--detailed", "-d", is_flag=True, show_default=True)
@click.option("--profile", "-p", help="AWS profile name")
@click.option("--region", "-r", help="AWS Region; use 'all' for all regions", default="ap-southeast-2", show_default=True)
@click.pass_context
def main_cli(ctx, subnetid, detailed, profile, region):
    ctx.obj = {"subnetid": subnetid, "region": region}
    start = time()
    try:
        if ctx.invoked_subcommand is not None:
            session = Session(profile_name=profile)
            account_id = session.client("sts").get_caller_identity()["Account"]
            process_account(session, profile, account_id, region, subnetid)
    finally:
        logging.info(f"Total execution time: {time() - start}s")
    

@main_cli.command(help="Process all accounts of the profiles in .aws/credentials")
@click.pass_context
def all(ctx):
    region, subnet_id = ctx.obj["region"], ctx.obj["subnetid"]
    accounts_processed = []
    for profile_name in read_aws_profile_names():
        try:
            session = Session(profile_name=profile_name)
            account_id = session.client("sts").get_caller_identity()["Account"]
            if account_id in accounts_processed:
                continue
            accounts_processed.append(account_id)
            
            if process_account(session, profile_name, account_id, region, subnet_id) is not None:
                break
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code in ["ExpiredToken"]:
                logging.warning(f"{profile_name} {error_code}. Skipped")
            else:
                raise


if __name__ == "__main__":
    main_cli(obj={})

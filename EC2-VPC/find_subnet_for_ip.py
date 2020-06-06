"""
Find which account/vpc/subnet that the given IP address belongs to.

Output: AccountId, Profile, Region, VpcId, SubnetId, CidrBlock
"""
from boto3.session import Session
from botocore.exceptions import ClientError
import click
import ipaddress
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


def process_account(session, profile, account_id, aws_region, ip):
    ip_addr = ipaddress.ip_address(ip)
    
    regions = session.get_available_regions("ec2") if aws_region == "all" else [aws_region]
    for region in regions:
        logging.debug(f"Checking {account_id} {profile} {region}")

        client = session.client("ec2", region_name=region)
        paginator = client.get_paginator("describe_subnets")
        for page in paginator.paginate():
            for item in page["Subnets"]:
                if ip_addr in ipaddress.ip_network(item["CidrBlock"]) is True:
                    print(account_id, profile, aws_region, item["VpcId"], item["SubnetId"], item["CidrBlock"])
                    return True


@click.command()
@click.option("--ip", "-i", help="IP address.", required=True)
@click.option("--profile", "-p", help="AWS profile name")
@click.option("--region", "-r", help="AWS Region; use 'all' for all regions", default="ap-southeast-2")
def main(ip, profile, region):
    start = time()
    try:
        accounts_processed = []
        profile_names = [profile] if profile else read_aws_profile_names()
        for profile_name in profile_names:
            try:
                session = Session(profile_name=profile_name)
                account_id = session.client("sts").get_caller_identity()["Account"]
                if account_id in accounts_processed:
                    continue
                accounts_processed.append(account_id)

                if process_account(session, profile_name, account_id, region, ip) is not None:
                    break
            except ClientError as e:
                error_code = e.response["Error"]["Code"]
                if error_code in ["AccessDenied", "ExpiredToken", "InvalidClientTokenId"]:
                    logging.warning(f"{profile_name} {error_code}. Skipped")
                else:
                    raise
    finally:
        logging.info(f"Total execution time: {time() - start}s")


if __name__ == "__main__":
    main()

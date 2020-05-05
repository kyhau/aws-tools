"""
Find which account/vpc/subnet that the given IP address belongs to.

Output: AccountId, Profile, Region, VpcId, SubnetId, CidrBlock
"""
from boto3.session import Session
from botocore.exceptions import ClientError
import click
from configparser import ConfigParser
import ipaddress
import logging
from os.path import expanduser, join

logging.getLogger().setLevel(logging.DEBUG)

aws_profiles = []
try:
    cp = ConfigParser()
    cp.read(join(expanduser("~"), ".aws", "credentials"))
    aws_profiles = cp.sections()
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
    accounts_processed = []
    profile_names = [profile] if profile else aws_profiles
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
            if error_code in ["ExpiredToken", "AccessDenied"]:
                logging.warning(f"{profile_name} {error_code}. Skipped")
            else:
                raise


if __name__ == "__main__": main()

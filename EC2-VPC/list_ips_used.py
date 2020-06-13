"""
Given a profile or a list of role arns, retrieve all IPs currently used in the corresponding account and write them to
a csv file (<account_id>_ips_used.csv).

Output data:
PrivateIpAddress, PrivateDnsName, IsPrimary, PublicIp, PublicDnsName, InstanceId, Description, AccountId, Region

`Description` is the instance's tag `Name` if the IP is used by an instance; otherwise it is the ENI description.
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


def dump(items, output_filename, to_console=True):
    with open(output_filename, "w") as f:
        for data in items:
            if to_console is True:
                print(data)
            f.write(f'{",".join(list(map(str, data)))}\n')


def get_ec2_tag_value(resp, tag="Name"):
    instance = resp["Reservations"][0]["Instances"][0]
    if "Tags" in instance:
        for t in instance["Tags"]:
            if t["Key"] == tag:
                return t["Value"]
    return None


def process_account(session, aws_region, account_id):
    results = []
    regions = session.get_available_regions("ec2") if aws_region == "all" else [aws_region]
    for region in regions:
        try:
            logging.debug(f"Checking {account_id} {region}")
            
            client = session.client("ec2", region_name=region)
            paginator = client.get_paginator("describe_network_interfaces")
            for page in paginator.paginate():
                for ni in page["NetworkInterfaces"]:
                    if ni["Status"] != "in-use":
                        continue
    
                    d1 = ni["Attachment"].get("InstanceId") if "Attachment" in ni else None
                    d2 = ni["Description"] if d1 is None else get_ec2_tag_value(client.describe_instances(InstanceIds=[d1]))
    
                    for data in ni["PrivateIpAddresses"]:
                        results.append([
                            data["PrivateIpAddress"],
                            data["PrivateDnsName"],
                            data["Primary"],
                            data["Association"].get("PublicIp") if "Association" in data else None,
                            data["Association"].get("PublicDnsName") if "Association" in data else None,
                            d1, d2, account_id, region
                        ])
        except ClientError as e:
            err_code = e.response["Error"]["Code"]
            if err_code in ["UnauthorizedOperation", "UnrecognizedClientException", "AuthFailure"]:
                logging.warning(f"Unable to process {account_id} {region}: {err_code}")
            else:
                raise

    if results:
        output_filename = f"{account_id}_ips_used.csv"
        titles = [
            "PrivateIpAddress", "PrivateDnsName", "IsPrimary", "PublicIp", "PublicDnsName", "InstanceId", "Description",
            "AccountId", "Region"]
        results.insert(0, titles)
        dump(results, output_filename)


@click.command()
@click.option("--profile", "-p", help="AWS profile name")
@click.option("--region", "-r", help="AWS Region; use 'all' for all regions", default="ap-southeast-2")
def main(profile, region):
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

                process_account(session, region, account_id)
            except ClientError as e:
                error_code = e.response["Error"]["Code"]
                if error_code in ["AccessDenied", "ExpiredToken"]:
                    logging.warning(f"{profile_name} {error_code}. Skipped")
                else:
                    raise
    finally:
        logging.info(f"Total execution time: {time() - start}s")


if __name__ == "__main__":
    main()

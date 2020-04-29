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
from configparser import ConfigParser
import logging
from os.path import expanduser, join


# Update the root logger to get messages at DEBUG and above
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger("botocore").setLevel(logging.CRITICAL)
logging.getLogger("boto3").setLevel(logging.CRITICAL)
logging.getLogger("urllib3").setLevel(logging.CRITICAL)

aws_profiles = []
try:
    cp = ConfigParser()
    cp.read(join(expanduser("~"), ".aws", "credentials"))
    aws_profiles = cp.sections()
except Exception as e:
    print(e)


def dump(data, output_filename, append=True, to_console=True):
    if to_console is True:
        print(data)
    with open(output_filename, "a" if append else "w") as f:
        f.write(f'{",".join(list(map(str, data)))}\n')


def get_ec2_tag_value(resp, tag="Name"):
    instance = resp["Reservations"][0]["Instances"][0]
    if "Tags" in instance:
        for t in instance["Tags"]:
            if t["Key"] == tag:
                return t["Value"]
    return None


def list_action(session, aws_region, account_id):
    output_filename = f"{account_id}_ips_used.csv"
    titles = [
        "PrivateIpAddress", "PrivateDnsName", "IsPrimary", "PublicIp", "PublicDnsName", "InstanceId", "Description",
        "AccountId", "Region"]
    dump(titles, output_filename, append=False)

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
                        ret = [
                            data["PrivateIpAddress"],
                            data["PrivateDnsName"],
                            data["Primary"],
                            data["Association"].get("PublicIp") if "Association" in data else None,
                            data["Association"].get("PublicDnsName") if "Association" in data else None,
                            d1, d2, account_id, region
                        ]
                        dump(ret, output_filename)
    
        except ClientError as e:
            if e.response["Error"]["Code"] in ["UnrecognizedClientException", "AuthFailure"]:
                logging.warning(f"Unable to process region {region}")
            else:
                raise


@click.command()
@click.option("--profile", "-p", help="AWS profile name")
@click.option("--region", "-r", help="AWS Region; use 'all' for all regions", default="ap-southeast-2")
def main(profile, region):
    accounts_processed = []
    profile_names = [profile] if profile else aws_profiles
    
    for profile_name in profile_names:
        session = Session(profile_name=profile_name)
        account_id = session.client("sts").get_caller_identity()["Account"]
        if account_id in accounts_processed:
            continue
        accounts_processed.append(account_id)
        
        list_action(session, region, account_id)


if __name__ == "__main__": main()

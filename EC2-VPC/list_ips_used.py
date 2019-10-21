"""
Given a profile or a list of role arns, retrieve all IPs currently used in the corresponding account and write them to
a csv file (<account_id>_ips_used.csv).

Output data:
PrivateIpAddress, PrivateDnsName, IsPrimary, PublicIp, PublicDnsName, InstanceId, Description, AccountId, Region

`Description` is the instance's tag `Name` if the IP is used by an instance; otherwise it is the ENI description.
"""
from boto3.session import Session
import click

from arki_common.aws import assume_role, read_role_arns_from_file
#from arki_common.utils import print_json


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


def list_action(session):
    account_id = session.client("sts").get_caller_identity()["Account"]

    output_filename = f"{account_id}_ips_used.csv"
    titles = [
        "PrivateIpAddress", "PrivateDnsName", "IsPrimary", "PublicIp", "PublicDnsName", "InstanceId", "Description",
        "AccountId", "Region"]
    dump(titles, output_filename, append=False)

    for region in session.get_available_regions("ec2"):
        #if region != "ap-southeast-2":
        #    continue
        print(f"Checking {account_id} {region}")

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


################################################################################
# Entry point

@click.command()
@click.option("--profile", "-p", default="default", help="AWS profile name")
@click.option("--rolesfile", "-f", help="File containing Role ARNs")
def main(profile, rolesfile):
    if rolesfile:
        for role_arn, acc_name in read_role_arns_from_file(filename=rolesfile):
            session = assume_role(role_arn=role_arn)
            list_action(session)
    else:
        session = Session(profile_name=profile)
        list_action(session)


if __name__ == "__main__": main()

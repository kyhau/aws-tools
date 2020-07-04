"""
Find which account/vpc/subnet that the given IP address belongs to.

Output: AccountId, Profile, Region, VpcId, SubnetId, CidrBlock
"""
import click
import ipaddress
import logging
from arki_common.aws import AwsApiHelper

logging.getLogger().setLevel(logging.DEBUG)


class Helper(AwsApiHelper):
    def process_request(self, session, account_id, region, kwargs):
        ip_addr = kwargs["ipaddress"]
        client = session.client("ec2", region_name=region)
        for item in self.paginate(client, "describe_subnets"):
            if ip_addr in ipaddress.ip_network(item["CidrBlock"]) is True:
                print(account_id, region, item["VpcId"], item["SubnetId"], item["CidrBlock"])
                return True


@click.command()
@click.option("--ip", "-i", required=True, help="IP address.")
@click.option("--profile", "-p", help="AWS profile name. Use profiles in ~/.aws if not specified.")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS Region. Use 'all' for all regions.")
def main(ip, profile, region):
    Helper().start(profile, region, "ec2", kwargs={"ipaddress": ipaddress.ip_address(ip)})


if __name__ == "__main__":
    main()

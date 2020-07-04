"""
List VPN Connections
"""
import click
import logging
import yaml
from arki_common.aws import AwsApiHelper

logging.getLogger().setLevel(logging.DEBUG)


class Helper(AwsApiHelper):
    def process_request(self, session, account_id, region, kwargs):
        client = session.client("ec2", region_name=region)
        items = client.describe_vpn_connections(**kwargs)["VpnConnections"]
        for item in items:
            print("--------------------------------------------------------------------------------")
            print(yaml.dump(item))
        if kwargs.get("VpnConnectionIds") and items:
            return True


@click.command()
@click.option("--vpcconnectionid", "-v", help="VPN Connection ID. Describe all VPC connections if not specified.")
@click.option("--profile", "-p", help="AWS profile name. Use profiles in ~/.aws if not specified.")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS Region. Use 'all' for all regions.")
def main(vpcconnectionid, profile, region):
    kwargs = {"VpnConnectionIds": [vpcconnectionid]} if vpcconnectionid else {}
    Helper().start(profile, region, "ec2", kwargs)


if __name__ == "__main__":
    main()

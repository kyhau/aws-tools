"""
List all or non-operational resolver endpoints and their IP addresses.
"""
import logging

import click

from helper.aws import AwsApiHelper

logging.getLogger().setLevel(logging.DEBUG)


class Helper(AwsApiHelper):
    def process_request(self, session, account_id, region, kwargs):
        client = session.client("route53resolver", region_name=region)
        for h in self.paginate(client, "list_resolver_endpoints", kwargs):
            print("ResolverEndpoint")
            print(h)
            print("IP Addresses")
            for i in self.paginate(client, "list_resolver_endpoint_ip_addresses", {"ResolverEndpointId": h["Id"]}):
                print(i)
            print("--------------------------------------------------------------------------------")


@click.command()
@click.option("--non-operational", "-n", is_flag=True, help="Show non-operational resolver endpoints only.")
@click.option("--profile", "-p", help="AWS profile name. Use profiles in ~/.aws if not specified.")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS Region. Use 'all' for all regions.")
def main(non_operational, profile, region):
    kwargs = {
        "Filters": [
            {"Name": "Status", "Values": ["CREATING" , "UPDATING", "AUTO_RECOVERING", "ACTION_NEEDED", "DELETING"]}
        ]
    } if non_operational is True else {}

    Helper().start(profile, region, "route53resolver", kwargs)


if __name__ == "__main__":
    main()

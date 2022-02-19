"""
Output: firehose name
"""
import logging

import click
from helper.aws import AwsApiHelper

logging.getLogger().setLevel(logging.DEBUG)


class Helper(AwsApiHelper):
    def __init__(self, detailed):
        super().__init__()
        self._detailed = detailed

    def process_request(self, session, account_id, region, kwargs):
        client = session.client("firehose", region_name=region)
        items = client.list_delivery_streams(**kwargs)["DeliveryStreamNames"]
        for item in client.list_delivery_streams(**kwargs)["DeliveryStreamNames"]:
            print(item)
        print(f"Total = {len(items)}")


@click.command()
@click.option("--detailed", "-d", show_default=True, is_flag=True, help="Show also AMI info.")
@click.option("--profile", "-p", help="AWS profile name. Use profiles in ~/.aws if not specified.")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS Region. Use 'all' for all regions.")
def main(detailed, profile, region):
    kwargs = {"Limit": 1000}
    Helper(detailed).start(profile, region, "firehose", kwargs)


if __name__ == "__main__":
    main()

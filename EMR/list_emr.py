import logging

import click
from helper.aws import AwsApiHelper

logging.getLogger().setLevel(logging.DEBUG)


class Helper(AwsApiHelper):
    def __init__(self, detailed):
        super().__init__()
        self._detailed = detailed

    def process_request(self, session, account_id, region, kwargs):
        client = session.client("emr", region_name=region)
        for item in self.paginate(client, "list_clusters", kwargs):
            print(item)


@click.command()
@click.option("--detailed", "-d", show_default=True, is_flag=True, help="Show also AMI info.")
@click.option("--profile", "-p", help="AWS profile name. Use profiles in ~/.aws if not specified.")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS Region. Use 'all' for all regions.")
def main(detailed, profile, region):
    Helper(detailed).start(profile, region, "emr", {})


if __name__ == "__main__":
    main()

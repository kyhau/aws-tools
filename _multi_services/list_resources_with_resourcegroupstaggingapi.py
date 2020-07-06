"""
aws resourcegroupstaggingapi get-resources --region

See also Config/list_resources_with_configservice.py
"""
import click
import logging
from arki_common.aws import AwsApiHelper

logging.getLogger().setLevel(logging.CRITICAL)


class Helper(AwsApiHelper):
    def process_request(self, session, account_id, region, kwargs):
        """Process request for a region of an account"""
        client = session.client("resourcegroupstaggingapi", region_name=region)
        for item in self.paginate(client, "get_resources", kwargs):
            arn = item["ResourceARN"]
            print(f"{account_id}, {region}, {arn}")


@click.command()
@click.option("--profile", "-p", help="AWS profile name. Use profiles in ~/.aws if not specified.")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS Region. Use 'all' for all regions.")
def main(profile, region):
    Helper().start(profile, region, "resourcegroupstaggingapi")


if __name__ == "__main__":
    main()

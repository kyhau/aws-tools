"""
A helper script to call describe_prefix_lists.
"""
import click
import logging
from arki_common.aws import AwsApiHelper

logging.getLogger().setLevel(logging.DEBUG)


class Helper(AwsApiHelper):
    def process_request(self, session, account_id, region, kwargs):
        cnt = 0
        client = session.client("ec2", region_name=region)
        for item in self.paginate(client, "describe_prefix_lists"):
            print(f'{item["PrefixListName"]}, {item["PrefixListId"]}, {item["Cidrs"]}')
            cnt += 1
        logging.debug(f"{account_id} {region}: Total items: {cnt}")


@click.command()
@click.option("--profile", "-p", help="AWS profile name. Use profiles in ~/.aws if not specified.")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS Region. Use 'all' for all regions.")
def main(profile, region):
    Helper().start(profile, region, "ec2")


if __name__ == "__main__":
    main()

import logging

import click
from helper.aws import AwsApiHelper

logging.getLogger().setLevel(logging.INFO)


class EcrHelper(AwsApiHelper):

    def process_request(self, session, account_id, region, kwargs):
        client = session.client("ecr", region_name=region)
        cnt = 0
        for item in self.paginate(client, "describe_repositories"):
            print(item)
            cnt += 1

        print(f"CheckPt: {account_id} {region} total = {cnt}")


@click.command()
@click.option("--profile", "-p", help="AWS profile name. Use profiles in ~/.aws if not specified.")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS Region. Use 'all' for all regions.")
def main(profile, region):
    EcrHelper().start(profile, region, "ecr")


if __name__ == "__main__":
    main()

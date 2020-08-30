"""
Output:
- List of Task Definition ARNs
Output (if `detailed` is specified):
- List of Task Definition ARNs and details
"""
import json
import logging

import click

from helper.aws import AwsApiHelper

logging.getLogger().setLevel(logging.DEBUG)


class Helper(AwsApiHelper):
    def __init__(self, detailed):
        super().__init__()
        self._detailed = detailed

    def process_request(self, session, account_id, region, kwargs):
        client = session.client("ecs", region_name=region)
        cnt = 0
        for arn in self.paginate(client, "list_task_definitions", kwargs):
            print(f"{cnt}: {arn}")
            if self._detailed:
                resp = client.describe_task_definition(taskDefinition=arn)
                print(json.dumps(resp["taskDefinition"], sort_keys=True, indent=2))
            cnt += 1


@click.command()
@click.option("--active", "-a", show_default=True, is_flag=True, help="Show Active only.")
@click.option("--detailed", "-d", show_default=True, is_flag=True, help="Show full Task Definition details.")
@click.option("--family", "-f", help="Family name.")
@click.option("--profile", "-p", help="AWS profile name. Use profiles in ~/.aws if not specified.")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS Region. Use 'all' for all regions.")
def main(active, detailed, family, profile, region):
    kwargs = {"sort": "DESC"}
    if family:
        kwargs["familyPrefix"] = family
    if active:
        kwargs["status"] = "ACTIVE"

    Helper(detailed).start(profile, region, "ecs", kwargs)


if __name__ == "__main__":
    main()

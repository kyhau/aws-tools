"""
1. List all layers' ARN and CompatibleRuntimes, or
2. List all layers' details if using --detailed, or
3. Lookup details of a layer by its name
"""
import json
import logging

import click
from helper.aws import AwsApiHelper

logging.getLogger().setLevel(logging.INFO)


class Helper(AwsApiHelper):
    def __init__(self, detailed):
        super().__init__()
        self._detailed = detailed

    def process_request(self, session, account_id, region, kwargs):
        layer_name = kwargs.get("LayerName", "").lower()
        client = session.client("lambda", region_name=region)
        for item in self.paginate(client, "list_layers", kwargs):
            if self._detailed:
                print(json.dumps(item, indent=2))
            else:
                print(f'{item.get("LayerArn")}, {item.get("LatestMatchingVersion", {}).get("CompatibleRuntimes")}')

            if layer_name and layer_name == item.get("LayerName", "").lower():
                return True


@click.command()
@click.option("--detailed", "-d", is_flag=True, default=False, help="Show details instead of just layer ARNs.")
@click.option("--name", "-n", help="Lambda layer name. List all layers if not specified.")
@click.option("--profile", "-p", help="AWS profile name. Use profiles in ~/.aws if not specified.")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS Region. Use 'all' for all regions.")
def main(detailed, name, profile, region):
    kwargs = {"LayerName": name} if name else {}
    Helper(detailed).start(profile, region, "lambda", kwargs)


if __name__ == "__main__":
    main()

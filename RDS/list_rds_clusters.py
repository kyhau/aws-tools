"""
List RDS clusters
1. Simple output: DatabaseName, DBClusterIdentifier, Status, Engine, Endpoint (primary)
2. With `-d`: print all details
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
        client = session.client("rds", region_name=region)

        for item in self.paginate(client, "describe_db_clusters", kwargs):
            if kwargs.get("DBClusterIdentifier"):
                print(json.dumps(item, indent=2, default=str))
                return

            if self._detailed:
                print(json.dumps(item, indent=2, default=str))
            else:
                print(", ".join([
                    item["DatabaseName"],
                    item["DBClusterIdentifier"],
                    item["Status"],
                    item["Engine"],
                    item["Endpoint"],
                ]))

@click.command()
@click.option("--clusterid", "-i", help="RDS cluster ID")
@click.option("--detailed", "-d", is_flag=True, show_default=True, help="Show all cluster details.")
@click.option("--profile", "-p", help="AWS profile name. Use profiles in ~/.aws if not specified.")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS Region. Use 'all' for all regions.")
def main(clusterid, detailed, profile, region):
    kwargs = {"DBClusterIdentifier": clusterid} if clusterid else {}
    Helper(detailed).start(profile, region, "rds", kwargs)


if __name__ == "__main__":
    main()

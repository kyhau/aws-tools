"""
List RDS cluster endpoints
"""
import json
import logging

import click
from helper.aws import AwsApiHelper

logging.getLogger().setLevel(logging.DEBUG)


class Helper(AwsApiHelper):
    def process_request(self, session, account_id, region, kwargs):
        client = session.client("rds", region_name=region)
        for item in self.paginate(client, "describe_db_cluster_endpoints", kwargs):
            print(json.dumps(item, indent=2, default=str))
            if kwargs.get("DBClusterIdentifier"):
                return

@click.command()
@click.option("--clusterid", "-i", help="RDS cluster ID")
@click.option("--profile", "-p", help="AWS profile name. Use profiles in ~/.aws if not specified.")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS Region. Use 'all' for all regions.")
def main(clusterid, profile, region):
    kwargs = {"DBClusterIdentifier": clusterid} if clusterid else {}
    Helper().start(profile, region, "rds", kwargs)


if __name__ == "__main__":
    main()

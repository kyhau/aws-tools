"""
Creates a dashboard if it does not already exist, or updates an existing dashboard.
If you update a dashboard, the entire contents are replaced.

If a dashboard with this name already exists, this call modifies that dashboard, replacing its current
contents. Otherwise, a new dashboard is created. The maximum length is 255, and valid characters are
A-Z, a-z, 0-9, "-", and "_". This parameter is required.
"""
import json
import logging

import click
from helper.aws import AwsApiHelper

logging.getLogger().setLevel(logging.INFO)
logging.getLogger("botocore").setLevel(logging.CRITICAL)
logging.getLogger("boto3").setLevel(logging.CRITICAL)


def read_json_file(filename):
    with open(filename) as f:
        return json.load(f)


class Helper(AwsApiHelper):
    def process_request(self, session, account_id, region, kwargs):
        resp = session.client("cloudwatch", region_name=region).put_dashboard(**kwargs)
        if resp["ResponseMetadata"]["HTTPStatusCode"] != 200:
            raise Exception("Failed to create CloudWatch Dashboard")


@click.command(help="Create or update CloudWatch Dashboard.")
@click.option("--dashboard-name", "-n", required=True, help="The name of the dashboard. If a dashboard with this name already exists, this call modifies that dashboard, replacing its current contents.")
@click.option("--dashboard-body-file", "-f", required=True, help="The detailed information about the dashboard in JSON.")
@click.option("--profile", "-p", help="AWS profile name. Use profiles in ~/.aws if not specified.")
@click.option("--region", "-r", required=True, help="AWS Region. All dashboards in your account are global, not region-specific.")
def main(dashboard_name, dashboard_body_file, profile, region):
    kwargs = {
        "DashboardName": dashboard_name,
        "DashboardBody": json.dumps(read_json_file(dashboard_body_file))
    }

    Helper().start(profile, region, "cloudwatch", kwargs)


if __name__ == "__main__":
    main()

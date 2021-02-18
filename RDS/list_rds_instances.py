"""
List RDS instances
Output: [
  [Account_id, DBInstanceIdentifier, DBInstanceStatus, Engine, Endpoint-Address,
   Endpoint-Port, IamAuthEnabled|IamAuthDisabled, MultiAZ|SingleAZ,
   PreferredMaintenanceWindow(UTC), CACertificateIdentifier],
]
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
        for item in self.paginate(client, "describe_db_instances", kwargs):
            if self._detailed:
                print(json.dumps(item, indent=2, default=str))
            else:
                data = [
                    account_id,
                    item["DBInstanceIdentifier"],
                    item["DBInstanceStatus"],
                    item["Engine"],
                    item["Endpoint"]["Address"],
                    str(item["Endpoint"]["Port"]),
                    "IamAuthEnabled" if item["IAMDatabaseAuthenticationEnabled"] else "IamAuthDisabled",
                    "MultiAZ" if item["MultiAZ"] else "SingleAZ",
                    item["PreferredMaintenanceWindow"],  # UTC
                    item.get("CACertificateIdentifier", "None"),
                ]
                print(",".join(data))

            if kwargs.get("InstanceIds"):
                return True


@click.command()
@click.option("--detailed", "-d", is_flag=True, show_default=True, help="Show all cluster details.")
@click.option("--instanceid", "-i", help="RDS instance ID")
@click.option("--profile", "-p", help="AWS profile name. Use profiles in ~/.aws if not specified.")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS Region. Use 'all' for all regions.")
def main(detailed, instanceid, profile, region):
    kwargs = {"InstanceIds": [instanceid]} if instanceid else {}
    Helper(detailed).start(profile, region, "rds", kwargs)


if __name__ == "__main__":
    main()

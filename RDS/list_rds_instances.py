"""
List RDS instances
Output: [
  [Account_id, Region, AWS-ProfileName, DBInstanceIdentifier, DBInstanceStatus, Engine, Endpoint-Address,
   Endpoint-Port, MultiAZ|SingleAZ, PreferredMaintenanceWindow(UTC), CACertificateIdentifier],
]
"""
import click
import logging
from arki_common.aws import AwsApiHelper

logging.getLogger().setLevel(logging.DEBUG)


class Helper(AwsApiHelper):
    def process_request(self, session, account_id, region, kwargs):
        client = session.client("rds", region_name=region)
        for item in self.paginate(client, "describe_db_instances", kwargs):
            data = [
                account_id,
                region,
                item["DBInstanceIdentifier"],
                item["DBInstanceStatus"],
                item["Engine"],
                item["Endpoint"]["Address"],
                str(item["Endpoint"]["Port"]),
                "MultiAZ" if item["MultiAZ"] else "SingleAZ",
                item["PreferredMaintenanceWindow"],  # UTC
                item.get("CACertificateIdentifier", "None"),
            ]
            print(",".join(data))
            
            if kwargs.get("InstanceIds"):
                return True


@click.command()
@click.option("--instanceid", "-i", help="RDS instance ID")
@click.option("--profile", "-p", help="AWS profile name. Use profiles in ~/.aws if not specified.")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS Region. Use 'all' for all regions.")
def main(instanceid, profile, region):
    kwargs = {"InstanceIds": [instanceid]} if instanceid else {}
    Helper().start(profile, region, "rds", kwargs)


if __name__ == "__main__":
    main()

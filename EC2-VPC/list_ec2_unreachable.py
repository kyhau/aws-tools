import click
import logging
from arki_common.aws import AwsApiHelper

logging.getLogger().setLevel(logging.DEBUG)


class Helper(AwsApiHelper):
    def process_request(self, session, account_id, region, kwargs):
        client = session.client("ec2", region_name=region)
        for item in self.paginate(client, "describe_instance_status", kwargs):
            print(account_id, region, item)

            if kwargs.get("InstanceIds"):
                return True

    def process_client_error(self, e, account_id, region):
        if e.response["Error"]["Code"] == "InvalidInstanceID.NotFound":
            pass
        else:
            super().process_client_error(e, account_id, region)


@click.command()
@click.option("--instanceid", "-i", help="EC2 instance ID. Describe all instances if not specified.")
@click.option("--profile", "-p", help="AWS profile name. Use profiles in ~/.aws if not specified.")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS Region. Use 'all' for all regions.")
def main(instanceid, profile, region):
    if instanceid:
        kwargs = {
            "InstanceIds": [instanceid],
        }
    else:
        kwargs = {
            "Filters": [
                {"Name": "instance-state-name", "Values": ["running"]},
                {"Name": "instance-status.reachability", "Values": ["failed"]},
                {"Name": "system-status.reachability", "Values": ["failed"]},
            ],
        }
    
    Helper().start(profile, region, "ec2", kwargs)


if __name__ == "__main__":
    main()

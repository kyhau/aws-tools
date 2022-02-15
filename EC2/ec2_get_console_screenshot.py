"""
Retrieve a JPG-format screenshot of a running instance to help with troubleshooting.
"""
import click
import logging
import os

from helper.aws import AwsApiHelper, get_tag_value


logging.getLogger().setLevel(logging.DEBUG)

OUTPUT_DIR = "ec2_console_screentshots"

os.makedirs(OSError, exist_ok=True)


class Helper(AwsApiHelper):
    def __init__(self):
        super().__init__()
    
    def process_request(self, session, account_id, region, kwargs):
        client = session.client("ec2", region_name=region)
        for item in self.paginate(client, "describe_instances", kwargs):
            for i in item["Instances"]:
                if i["State"]["Name"] == "running":
                    id = instance["InstanceId"]
                    filename = os.path.join(OUTPUT_DIR, f"{id}.jpeg")
                    response = ec2.get_console_screenshot(InstanceId=id, WakeUp=True)
                    with open(filename, "wb") as f:
                        f.write(base64.b64decode(response["ImageData"]))

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
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS Region. Use "all" for all regions.")
def main(instanceid, profile, region):
    kwargs = {"InstanceIds": [instanceid]} if instanceid else {}
    Helper().start(profile, region, "ec2", kwargs)


if __name__ == "__main__":
    main()

"""
Output: account_id, region, instance_id, private_ip, public_ip
"""
import click
import logging
from arki_common.aws import AwsApiHelper, get_tag_value

logging.getLogger().setLevel(logging.DEBUG)


class Helper(AwsApiHelper):
    def __init__(self, detailed):
        super().__init__()
        self._amis_known = {}
        self._detailed = detailed

    def get_image(self, ami_id, client):
        if ami_id not in self._amis_known:
            try:
                image = client.describe_images(ImageIds=[ami_id])["Images"][0]
                self._amis_known[ami_id] = [
                    image.get("Name", "NoName"),
                    "Public" if image["Public"] is True else "Private",
                ]
            except:
                self._amis_known[ami_id] = ["NoAMIName", "UnknownAMI"]
        return self._amis_known[ami_id]
    
    def process_request(self, session, account_id, region, kwargs):
        client = session.client("ec2", region_name=region)
        for item in self.paginate(client, "describe_instances", kwargs):
            for i in item["Instances"]:
                data = [
                    account_id,
                    region,
                    i["InstanceId"],
                    get_tag_value(i["Tags"]),
                    i.get("Platform", "Linux/UNIX"),
                    i.get("PrivateIpAddress"),
                    i.get("PublicIpAddress", "NoPublicIP"),
                ]
                if self._detailed:
                    data += self.get_image(i["ImageId"], client)
                print(",".join(data))

                if kwargs.get("InstanceIds"):
                    return True

    def process_client_error(self, e, account_id, region):
        if e.response["Error"]["Code"] == "InvalidInstanceID.NotFound":
            pass
        else:
            super().process_client_error(e, account_id, region)


@click.command()
@click.option("--detailed", "-d", show_default=True, is_flag=True, help="Show also AMI info.")
@click.option("--instanceid", "-i", help="EC2 instance ID. Describe all instances if not specified.")
@click.option("--profile", "-p", help="AWS profile name. Use profiles in ~/.aws if not specified.")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS Region. Use 'all' for all regions.")
def main(detailed, instanceid, profile, region):
    kwargs = {"InstanceIds": [instanceid]} if instanceid else {}
    Helper(detailed).start(profile, region, "ec2", kwargs)


if __name__ == "__main__":
    main()

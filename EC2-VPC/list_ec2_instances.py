"""
Output:
- default: account_id, region, instance_id, name, platform, private_ip, public_ip, image_id (in one line)
- show_all: all ec2 info (in json)
- show_ami: include also ImageName and ImageIsPublic
"""
import json
import logging

import click
from helper.aws import AwsApiHelper, get_tag_value

logging.getLogger().setLevel(logging.DEBUG)


class Helper(AwsApiHelper):
    def __init__(self, show_all, show_ami):
        super().__init__()
        self._amis_known = {}
        self._show_all = show_all
        self._show_ami = show_ami

    def get_image(self, ami_id, client):
        if ami_id not in self._amis_known:
            self._amis_known[ami_id] = {"ImageName": "NoName", "ImageIsPublic": True}
            try:
                image = client.describe_images(ImageIds=[ami_id])["Images"][0]
                self._amis_known[ami_id] = {
                    "ImageName": image.get("Name", "NoName"),
                    "ImageIsPublic": image["Public"] is True,
                }
            except:
                pass
        return self._amis_known[ami_id]

    def process_request(self, session, account_id, region, kwargs):
        client = session.client("ec2", region_name=region)
        for item in self.paginate(client, "describe_instances", kwargs):
            for i in item["Instances"]:
                if self._show_all:
                    if self._show_ami:
                        i.update(self.get_image(i["ImageId"], client))
                    data = {i["InstanceId"]: i}
                    print(json.dumps(data, default=str, indent=2, sort_keys=True))
                else:
                    data = [
                        account_id,
                        region,
                        i["InstanceId"],
                        get_tag_value(i["Tags"]),
                        i.get("Platform", "Linux/UNIX"),
                        i.get("PrivateIpAddress", "None"),
                        i.get("PublicIpAddress", "None"),
                    ]
                    if self._show_ami:
                        ret = self.get_image(i["ImageId"], client)
                        data.append(ret["ImageName"])
                        data.append(str(ret["ImageIsPublic"]))
                    print(", ".join(data))

                if kwargs.get("InstanceIds"):
                    return True

    def process_client_error(self, e, account_id, region):
        if e.response["Error"]["Code"] == "InvalidInstanceID.NotFound":
            pass
        else:
            super().process_client_error(e, account_id, region)


@click.command()
@click.option("--instance-id", "-i", help="EC2 instance ID. Describe all instances if not specified.")
@click.option("--show-all", "-d", show_default=True, is_flag=True, help="Show all instance info.")
@click.option("--show-ami", "-a", show_default=True, is_flag=True, help="Show also AMI info.")
@click.option("--profile", "-p", help="AWS profile name. Use profiles in ~/.aws if not specified.")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS Region. Use 'all' for all regions.")
def main(instance_id, show_all, show_ami, profile, region):
    kwargs = {"InstanceIds": [instance_id]} if instance_id else {}

    if not show_all:
        line = "account_id, region, instance_id, platform, name, private_ip, public_ip, image_id"
        if show_ami:
            line += ", image_name, image_is_public"
        print(line)

    Helper(show_all, show_ami).start(profile, region, "ec2", kwargs)


if __name__ == "__main__":
    main()

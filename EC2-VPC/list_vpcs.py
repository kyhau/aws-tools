"""
List VPCs or find a VPC by ID
"""
import click
import logging
import yaml
from arki_common.aws import AwsApiHelper

logging.getLogger().setLevel(logging.DEBUG)


class Helper(AwsApiHelper):
    def process_request(self, session, account_id, region, kwargs):
        client = session.client("ec2", region_name=region)
        for item in AwsApiHelper.paginate(client,"describe_vpcs", kwargs):
            print("--------------------------------------------------------------------------------")
            print(yaml.dump(item))
            if kwargs.get("VpcIds"):
                return True

    def process_client_error(self, e, account_id, region):
        if e.response["Error"]["Code"] == "InvalidVpcID.NotFound":
            pass
        else:
            super().process_client_error(e, account_id, region)


@click.command()
@click.option("--vpcid", "-v", help="VPC ID. Describe all VPCs if not specified.")
@click.option("--profile", "-p", help="AWS profile name. Use profiles in ~/.aws if not specified.")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS Region. Use 'all' for all regions.")
def main(vpcid, profile, region):
    kwargs = {"VpcIds": [vpcid]} if vpcid else {}
    Helper().start(profile, region, "ec2", kwargs)


if __name__ == "__main__":
    main()

"""
Output:
SubnetId, AvailabilityZone, CidrBlock, usable=(num), used=(num), available=(num),
"""
import logging

import click

from arki_common.aws import AwsApiHelper

logging.getLogger().setLevel(logging.DEBUG)


class Helper(AwsApiHelper):
    def __init__(self, threshold):
        super().__init__()
        self._threshold = threshold

    def process_request(self, session, account_id, region, kwargs):
        client = session.client("ec2", region_name=region)
        cnt = 0
        for item in self.paginate(client, "describe_subnets", kwargs):
            mask = int(item["CidrBlock"].split("/")[1])
            # 5 addresses reserved per subnet: .0 network, .1 VPC router, .2 DNS, .3 future, .255 broadcast
            # https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html
            usable_ip_cnt = 2 ** (32 - mask) - 5
            available_ip_cnt = item["AvailableIpAddressCount"]

            data = [
                item["SubnetId"],
                item["AvailabilityZone"],
                item["CidrBlock"],
                f"usable={usable_ip_cnt}",
                f"used={usable_ip_cnt - available_ip_cnt}",
                f"available={available_ip_cnt}",
                "***" if usable_ip_cnt < self._threshold else "",
            ]
            print(", ".join(data))
            cnt += 1

        if cnt and kwargs.get("SubnetIds"):
            return cnt


@click.command()
@click.option("--subnetid", "-s", help="Subnet ID. Describe all subnets if not specified.")
@click.option("--threshold", "-t", default=8, show_default=True, help="Highlight subnet count if number of available IP address is less than this threshold.")
@click.option("--profile", "-p", help="AWS profile name. Use profiles in ~/.aws if not specified.")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS Region. Use 'all' for all regions.")
def main(subnetid, threshold, profile, region):
    kwargs = {"SubnetIds": [subnetid]} if subnetid else {}
    Helper(threshold).start(profile, region, "ec2", kwargs)


if __name__ == "__main__":
    main()

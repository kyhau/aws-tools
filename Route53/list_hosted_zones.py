"""
List/find hosted zones and vpcs
"""
import click
import logging
from helper.aws import AwsApiHelper

logging.getLogger().setLevel(logging.DEBUG)


class Helper(AwsApiHelper):
    def __init__(self, vpc_id, detailed):
        super().__init__()
        self._vpc_id = vpc_id
        self._detailed = detailed

    def process_request(self, session, account_id, region, kwargs):
        if self._detailed is False:
            print(",".join(["Name", "PubOrPri", "ResourceRecordSetCount", "NameServers", "VPCs", "Id", "Comment"]))

        client = session.client("route53", region_name=region)
        for h in self.paginate(client, "list_hosted_zones", kwargs):
            hz = client.get_hosted_zone(Id=h["Id"])
            if not self._vpc_id or any(d["VPCId"] == self._vpc_id for d in hz.get("VPCs", {})):
                if self._detailed:
                    del hz["ResponseMetadata"]
                    data = {h["Name"]: hz}
                    print(data)
                else:
                    data = [
                        h["Name"],
                        "private" if h["Config"]["PrivateZone"] else "public",
                        str(h["ResourceRecordSetCount"]),
                        str(hz.get("DelegationSet",{}).get("NameServers")),
                        str(hz.get("VPCs")),
                        h["Id"],
                        h["Config"]["Comment"],
                    ]
                    print(",".join(data))


@click.command()
@click.option("--detailed", "-d", show_default=True, is_flag=True, help="Show more details.")
@click.option("--vpcid", "-v", help="VPC ID. List only hosted zones that a specified VPC is associated with.")
@click.option("--profile", "-p", help="AWS profile name. Use profiles in ~/.aws if not specified.")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS Region. Use 'all' for all regions.")
def main(detailed, vpcid, profile, region):
    Helper(vpcid, detailed).start(profile, region, "route53")


if __name__ == "__main__":
    main()

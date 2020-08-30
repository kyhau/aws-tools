"""
List Security Groups
"""
import click
import logging
import yaml
from helper.aws import AwsApiHelper

logging.getLogger().setLevel(logging.DEBUG)


class Helper(AwsApiHelper):
    def process_request(self, session, account_id, region, kwargs):
        # Do not use "GroupNames"
        # --group-names option is applied ONLY to the default VPC, and otherwise you have to use the filters to query
        group_name = kwargs.pop("GroupNames") if "GroupNames" in kwargs else None
        cnt = 0
        client = session.client("ec2", region_name=region)
        for item in AwsApiHelper.paginate(client, "describe_security_groups", kwargs):
            if group_name is None or item["GroupName"].lower() == group_name:
                print("--------------------------------------------------------------------------------")
                print(yaml.dump(item))
                cnt += 1
        logging.debug(f"Total: {cnt}")
        if cnt and (kwargs.get("GroupIds") or group_name):
            return cnt


@click.command()
@click.option("--groupid", "-i", help="Security Group ID. Describe all security groups if not specified.")
@click.option("--groupname", "-n", help="Security Group Name. Describe all security groups if not specified.")
@click.option("--profile", "-p", help="AWS profile name. Use profiles in ~/.aws if not specified.")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS Region. Use 'all' for all regions.")
def main(groupid, groupname, profile, region):
    kwargs = {}
    if groupid:
        kwargs["GroupIds"] = [groupid]
    if groupname:
        kwargs["GroupNames"] = groupname.lower()
    Helper().start(profile, region, "ec2", kwargs)


if __name__ == "__main__":
    main()

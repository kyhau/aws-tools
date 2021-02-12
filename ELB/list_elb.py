import logging

import click
from helper.aws import AwsApiHelper, get_tag_value

logging.getLogger().setLevel(logging.DEBUG)


class ElbHelper(AwsApiHelper):
    def __init__(self, detailed):
        super().__init__()
        self._detailed = detailed

    def process_request(self, session, account_id, region, kwargs):
        client = session.client("elb", region_name=region)
        for item in self.paginate(client, "describe_load_balancers", kwargs):
            print(item)
            # TODO format results and include tags

    def get_tags(self, item):
        return self._client.describe_tags(LoadBalancerNames=[item["LoadBalancerName"]])["TagDescriptions"][0]["Tags"]


class ElbV2Helper(ElbHelper):
    def process_request(self, session, account_id, region, kwargs):
        client = session.client("elbv2", region_name=region)
        for item in self.paginate(client, "describe_load_balancers", kwargs):
            print(item)
            # TODO format results and include tags

    def get_tags(self, item):
        return self._client.describe_tags(ResourceArns=[item["LoadBalancerArn"]])["TagDescriptions"][0]["Tags"]


@click.command()
@click.option("--detailed", "-d", show_default=True, is_flag=True, help="Show also AMI info.")
@click.option("--instanceid", "-i", help="EC2 instance ID. Describe all instances if not specified.")
@click.option("--profile", "-p", help="AWS profile name. Use profiles in ~/.aws if not specified.")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS Region. Use 'all' for all regions.")
def main(detailed, instanceid, profile, region):
    kwargs = {"InstanceIds": [instanceid]} if instanceid else {}
    ElbHelper(detailed).start(profile, region, "elb", kwargs)
    ElbV2Helper(detailed).start(profile, region, "elbv2", kwargs)


if __name__ == "__main__":
    main()

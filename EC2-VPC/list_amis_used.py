"""
Output:
{
    account_id: {
        region: {
            "ami_id": {
                "asg": set(asg_name),
                "ec2": set(instance_id),
            }
        }
    }
}
"""
import click
from collections import defaultdict
import logging
from helper.aws import AwsApiHelper

logging.getLogger().setLevel(logging.DEBUG)


class Helper(AwsApiHelper):
    def __init__(self, ):
        super().__init__()
        self.results = defaultdict(dict)

    def amis_used_by_ec2(self, session, region, region_dict):
        """Find AMIs referenced in EC2 instances"""
        client = session.client("ec2", region_name=region)
        for item in self.paginate(client, "describe_instances"):
            for instance in item["Instances"]:
                if instance["State"]["Name"] in ["pending", "running"]:
                    region_dict[instance["ImageId"]]["ec2"].add(instance["InstanceId"])
        return region_dict
    
    def amis_used_by_asg(self, session, region, region_dict):
        """Find AMIs referenced in Auto Scaling Groups"""
        client = session.client("autoscaling", region_name=region)

        # Retrieve auto scaling groups' launch configuration names
        launch_conf_asg = defaultdict(set)
        for asg in self.paginate(client, "describe_auto_scaling_groups"):
            launch_conf_asg[asg["LaunchConfigurationName"]].add(asg["AutoScalingGroupName"])
    
        paginator = client.get_paginator("describe_launch_configurations")
        for page in paginator.paginate(LaunchConfigurationNames=list(launch_conf_asg.keys())):
            for launch_config in page["LaunchConfigurations"]:
                region_dict[launch_config["ImageId"]]["asg"] = launch_conf_asg[launch_config["LaunchConfigurationName"]]
        return region_dict
        
    def process_request(self, session, account_id, region, kwargs):
        region_dict = defaultdict(lambda: defaultdict(set))
        
        def dump(region_dict, name):
            for ami_id, v in region_dict.items():
                for id in v[name]:
                    print(f"{account_id}, {region}, {ami_id}, {name}, {id}")
        
        # Find AMIs referenced in EC2 instances
        region_dict = self.amis_used_by_ec2(session, region, region_dict)
        dump(region_dict, "ec2")
    
        # Find AMIs referenced in Auto Scaling Groups
        region_dict = self.amis_used_by_asg(session, region, region_dict)
        dump(region_dict, "asg")

        self.results[account_id][region] = region_dict


@click.command()
@click.option("--vpcid", "-v", help="VPC ID. Describe all VPCs if not specified.")
@click.option("--profile", "-p", help="AWS profile name. Use profiles in ~/.aws if not specified.")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS Region. Use 'all' for all regions.")
def main(vpcid, profile, region):
    kwargs = {"VpcIds": [vpcid]} if vpcid else {}
    Helper().start(profile, region, "ec2", kwargs)


if __name__ == "__main__":
    main()

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
from boto3.session import Session
from botocore.exceptions import ClientError
import click
from collections import defaultdict
from configparser import ConfigParser
import logging
from os.path import expanduser, join

logging.getLogger().setLevel(logging.DEBUG)

aws_profiles = []
try:
    cp = ConfigParser()
    cp.read(join(expanduser("~"), ".aws", "credentials"))
    aws_profiles = cp.sections()
except Exception as e:
    logging.error(e)


def process_account(session, account_id, aws_region, results):
    regions = session.get_available_regions("ec2") if aws_region == "all" else [aws_region]
    for region in regions:
        logging.debug(f"Checking {account_id} {region}")
        region_dict = defaultdict(lambda: defaultdict(set))

        try:
            ################################################################################
            # Find AMIs referenced in EC2 instances
            client = session.client("ec2", region_name=region)
            paginator = client.get_paginator("describe_instances")
            for page in paginator.paginate():
                for item in page["Reservations"]:
                    for instance in item["Instances"]:
                        if instance['State']["Name"] in ["pending", "running"]:
                            region_dict[instance["ImageId"]]["ec2"].add(instance['InstanceId'])
            # Print
            for ami_id, v in region_dict.items():
                for iid in v["ec2"]:
                    print(f"{account_id}, {region}, {ami_id}, ec2, {iid}")

            ################################################################################
            # Find AMIs referenced in Auto Scaling Groups
            client = session.client("autoscaling", region_name=region)
            # Retrieve auto scaling groups' launch configuration names
            launch_conf_asg = defaultdict(set)
            paginator = client.get_paginator("describe_auto_scaling_groups")
            for page in paginator.paginate():
                for asg in page["AutoScalingGroups"]:
                    launch_conf_asg[asg["LaunchConfigurationName"]].add(asg["AutoScalingGroupName"])

            paginator = client.get_paginator("describe_launch_configurations")
            for page in paginator.paginate(LaunchConfigurationNames=list(launch_conf_asg.keys())):
                for launch_config in page["LaunchConfigurations"]:
                    region_dict[launch_config["ImageId"]]["asg"] = launch_conf_asg[launch_config["LaunchConfigurationName"]]

            # Print
            for ami_id, v in region_dict.items():
                for asg_name in v["asg"]:
                    print(f"{account_id}, {region}, {ami_id}, asg, {asg_name}")

        except ClientError as e:
            if e.response["Error"]["Code"] == "UnrecognizedClientException":
                logging.warning(f"Unable to process region {region}")
            else:
                raise
        except Exception as e:
            logging.error(e)

        results[account_id][region] = region_dict

    return results


@click.command()
@click.option("--profile", "-p", help="AWS profile name")
@click.option("--region", "-r", help="AWS Region; use 'all' for all regions", default="ap-southeast-2")
def main(profile, region):
    accounts_processed = []
    profile_names = [profile] if profile else aws_profiles
    results = defaultdict(dict)
    for profile_name in profile_names:
        try:
            session = Session(profile_name=profile_name)
            account_id = session.client("sts").get_caller_identity()["Account"]
            if account_id in accounts_processed:
                continue
            accounts_processed.append(account_id)
            
            process_account(session, account_id, region, results)
        
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code in ["ExpiredToken", "AccessDenied"]:
                logging.warning(f"{profile_name} {error_code}. Skipped")
            else:
                raise


if __name__ == "__main__": main()

from boto3.session import Session
import click
from collections import defaultdict

from arki_common.aws import assume_role, read_role_arns_from_file, DEFAULT_ROLE_ARNS_FILE


def list_action(session, results):
    account_id = session.client("sts").get_caller_identity()["Account"]
    if account_id in results:
        return

    for region in session.get_available_regions("ec2"):
        print(f"Checking {account_id} {region}")
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
        except Exception as e:
            print(e)

        results[account_id][region] = region_dict

    return results


################################################################################
# Entry point

@click.command()
@click.option("--profile", "-p", help="AWS profile name")
@click.option("--rolesfile", "-f", default=DEFAULT_ROLE_ARNS_FILE, help="Files containing Role ARNs")
def main(profile, rolesfile):
    results = defaultdict(dict)
    """ Example:
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

    if profile is not None:
        session = Session(profile_name=profile)
        list_action(session, results)

    for role_arn in read_role_arns_from_file(filename=rolesfile):
        session = assume_role(role_arn=role_arn)
        list_action(session, results)


if __name__ == "__main__": main()

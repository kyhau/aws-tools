"""
A simple script to ...
"""
from boto3.session import Session
import click
import yaml
#boto3.setup_default_session(profile_name=AWS_PROFILE)


@click.command(help="Help 1")
@click.option("--clusterarn", "-c", required=True, help="ARN of MSK cluster")
@click.option("--profile", "-p", default="default", show_default=True, help="AWS profile name")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS Region; use 'all' for all regions")
@click.option("--detailed", "-d", show_default=True, is_flag=True)
def main(clusterarn, profile, region, detailed):
    session = Session(profile_name=profile)
    client = session.client("kafka", region_name=region)
    
    paginator = client.get_paginator("list_nodes")
    for page in paginator.paginate(ClusterArn=clusterarn):
        for item in page["NodeInfoList"]:
            print("--------------------------------------------------------------------------------")
            print(yaml.dump(item))


if __name__ == "__main__":
    main()
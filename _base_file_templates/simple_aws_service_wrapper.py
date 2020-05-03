"""
A simple script to ...
"""
from boto3.session import Session
import click
import yaml


@click.command()
@click.option("--clusterarn", "-c", help="ARN of MSK cluster", required=True)
@click.option("--profile", "-p", help="AWS profile name", default="default")
@click.option("--region", "-r", help="AWS Region; use 'all' for all regions", default="ap-southeast-2")
@click.option("--detailed", "-d", is_flag=True)
def main(clusterarn, profile, region, detailed):
    session = Session(profile_name=profile)
    client = session.client("kafka", region_name=region)
    
    paginator = client.get_paginator("list_nodes")
    for page in paginator.paginate(ClusterArn=clusterarn):
        for item in page["NodeInfoList"]:
            print("--------------------------------------------------------------------------------")
            print(yaml.dump(item))


if __name__ == "__main__": main()
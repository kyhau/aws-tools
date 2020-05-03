"""
Ref: https://docs.aws.amazon.com/msk/1.0/apireference/clusters-clusterarn-nodes.html#ListNodes
"""
from boto3.session import Session
import click
import yaml


@click.command()
@click.option("--profile", "-p", help="AWS profile name", default="default")
@click.option("--clusterarn", "-c", help="ARN of MSK cluster", required=True)
@click.option("--region", "-r", help="AWS Region; use 'all' for all regions", default="ap-southeast-2")
def main(profile, clusterarn, region):
    session = Session(profile_name=profile)
    client = session.client("kafka", region_name=region)

    paginator = client.get_paginator("list_nodes")
    for page in paginator.paginate(ClusterArn=clusterarn):
        for item in page["NodeInfoList"]:
            print("--------------------------------------------------------------------------------")
            print(yaml.dump(item))


if __name__ == "__main__": main()
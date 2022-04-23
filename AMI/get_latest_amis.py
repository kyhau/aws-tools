"""
bash:
aws ssm get-parameters-by-path --path "/aws/service/ami-amazon-linux-latest" | jq '.Parameters[] | "\(.Value) \(.Version) \(.ARN)"'
aws ssm get-parameters-by-path --path "/aws/service/ami-windows-latest" | jq '.Parameters[] | "\(.Value) \(.Version) \(.ARN)"'

aws ssm get-parameters "$@" --names /aws/service/ecs/optimized-ami/amazon-linux-2/recommended/image_id --query "Parameters[0].Value" --output text
aws ssm get-parameters "$@" --names /aws/service/eks/optimized-ami/1.14/amazon-linux-2/recommended/image_id --query "Parameters[0].Value" --output text
"""
import json

import click
from boto3.session import Session
from helper.selector import prompt_multi_selection


def get_ecs_meta_dict():
    # https://docs.aws.amazon.com/AmazonECS/latest/developerguide/retrieve-ecs-optimized_AMI.html
    return {
        "/aws/service/ecs/optimized-ami/amazon-linux": "Amazon ECS-optimized Amazon Linux (x86_64) AMI deprecated as of 2021-04-15",
        "/aws/service/ecs/optimized-ami/amazon-linux-2": "Amazon ECS-Optimized Amazon Linux 2 (x86_64) AMI",
        "/aws/service/ecs/optimized-ami/amazon-linux-2/arm64": "Amazon ECS-Optimized Amazon Linux 2 (arm64) AMI",
        "/aws/service/ecs/optimized-ami/amazon-linux-2/gpu": "Amazon ECS-Optimized Amazon Linux 2 (GPU) AMI",
        "/aws/service/ecs/optimized-ami/amazon-linux-2/inf": "Amazon ECS-Optimized Amazon Linux 2 (Inferentia) AMI",
        "/aws/service/ecs/optimized-ami/amazon-linux-2022": "Amazon ECS-Optimized Amazon Linux 2022 (x86_64) AMI"
    }


def get_eks_meta_dict():
    # https://docs.aws.amazon.com/eks/latest/userguide/eks-linux-ami-versions.html
    K8S_VERSIONS = [
        "1.22",
        "1.21",
        "1.20",
        "1.19",
        "1.18",
        "1.17",
    ]

    # https://docs.aws.amazon.com/eks/latest/userguide/retrieve-ami-id.html
    ami_variants = {}
    for k8s_version in K8S_VERSIONS:
        ami_variants[f"/aws/service/eks/optimized-ami/{k8s_version}/amazon-linux-2"] = "Amazon EKS-optimized Amazon Linux 2 (x86_64) AMI"
        ami_variants[f"/aws/service/eks/optimized-ami/{k8s_version}/amazon-linux-2-arm64"] = "Amazon EKS-optimized Amazon Linux 2 (arm64) AMI"
        ami_variants[f"/aws/service/eks/optimized-ami/{k8s_version}/amazon-linux-2-gpu"] = "Amazon EKS-optimized Amazon Linux 2 (GPU) AMI"

    return ami_variants


def get_parameters_by_path(param_path, region, session):
    params = {}
    for region in session.get_available_regions("ssm") if region == "all" else [region]:
        try:
            client = session.client("ssm", region_name=region)
            for page in client.get_paginator("get_parameters_by_path").paginate(Path=param_path):
                for p in page["Parameters"]:
                    params[p["ARN"]] = p
                    #print(f'{p["Value"]}, {p["Version"]}, {p["LastModifiedDate"]}, {p["ARN"]}')
        except Exception as e:
            print(f"Skip region {region} due to error: {e}")
    return params


def get_parameters(param_path, region, session):
    for region in session.get_available_regions("ssm") if region == "all" else [region]:
        try:
            client = session.client("ssm", region_name=region)
            for item in client.get_parameters(Names=[param_path])["Parameters"]:
                v = item.pop("Value")
                del item["Name"]
                del item["Type"]
                item.update(json.loads(v))
                print(json.dumps(item, default=str, indent=2, sort_keys=True))
        except Exception as e:
            print(f"Skip region {region} due to error: {e}")


@click.group(help="List the lastest AWS managed AMIs")
@click.option("--profile", "-p", default="default", show_default=True, help="AWS profile name")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS region, or 'all' for all regions")
@click.pass_context
def cli_main(ctx, profile, region):
    session = Session(profile_name=profile)
    ctx.obj = {"session": session, "region": region}


@cli_main.command(help="Find EC2 Linux AMIs")
@click.pass_context
def ec2(ctx):
    region, session = ctx.obj["region"], ctx.obj["session"]
    data = get_parameters_by_path(param_path="/aws/service/ami-amazon-linux-latest", region=region, session=session)
    resp = prompt_multi_selection("AMI", options=list(data.keys()), pre_selected_options=[])
    for arn in resp["AMIs"]:
        print(json.dumps(data[arn], default=str, indent=2, sort_keys=True))


@cli_main.command(help="Find ECS AMIs")
@click.pass_context
def ecs(ctx):
    region, session = ctx.obj["region"], ctx.obj["session"]
    resp = prompt_multi_selection("AMI", options=list(get_ecs_meta_dict().keys()), pre_selected_options=[])
    for name in resp["AMIs"]:
        get_parameters(param_path=f"{name}/recommended", region=region, session=session)


@cli_main.command(help="Find EKS AMIs")
@click.pass_context
def eks(ctx):
    region, session = ctx.obj["region"], ctx.obj["session"]
    resp = prompt_multi_selection("AMI", options=list(get_eks_meta_dict().keys()), pre_selected_options=[])
    for name in resp["AMIs"]:
        get_parameters(param_path=f"{name}/recommended", region=region, session=session)


@cli_main.command(help="Find EC2 Windows AMIs")
@click.pass_context
def windows(ctx):
    region, session = ctx.obj["region"], ctx.obj["session"]
    data = get_parameters_by_path(param_path="/aws/service/ami-windows-latest", region=region, session=session)
    resp = prompt_multi_selection("AMI", options=list(data.keys()), pre_selected_options=[])
    for arn in resp["AMIs"]:
        print(json.dumps(data[arn], default=str, indent=2, sort_keys=True))


if __name__ == "__main__":
    cli_main(obj={})

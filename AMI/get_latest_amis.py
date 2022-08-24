"""
Find AMI ID of the latest
- ECS optimized Bottlerocket AMIs
- EKS optimized Bottlerocket AMIs
- EC2 Linux AMIs
- ECS optimized Amazon Linux 1/2 AMIs
- EKS optimized Amazon Linux 2 AMIs
- EC2 Windows AMIs
"""
import json

import click
from boto3.session import Session
from helper.selector import prompt_multi_selection


def get_bottlerocket_ecs_meta_dict():
    # https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-bottlerocket.html
    return {
        "/aws/service/bottlerocket/aws-ecs-1/arm64": "Amazon ECS-Optimized Bottlerocket (arm64) AMI",
        "/aws/service/bottlerocket/aws-ecs-1/x86_64": "Amazon ECS-Optimized Bottlerocket (x86_64) AMI",
        "/aws/service/bottlerocket/aws-ecs-1-nvidia/arm64": "Amazon ECS-Optimized (NVIDIA GPU support) Bottlerocket (arm64) AMI",
        "/aws/service/bottlerocket/aws-ecs-1-nvidia/x86_64": "Amazon ECS-Optimized (NVIDIA GPU support) Bottlerocket (x86_64) AMI",
    }


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


def get_eks_meta_dict(get_bottlerocket=False):
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
    if get_bottlerocket:
        for k8s_version in K8S_VERSIONS:
            ami_variants[f"/aws/service/bottlerocket/aws-k8s-{k8s_version}/arm64"] = "Amazon EKS-optimized Bottlerocket (arm64 Standard) AMI"
            ami_variants[f"/aws/service/bottlerocket/aws-k8s-{k8s_version}/x86_64"] = "Amazon EKS-optimized Bottlerocket (x86_64 Standard) AMI"
            ami_variants[f"/aws/service/bottlerocket/aws-k8s-{k8s_version}-nvidia/arm64"] = "Amazon EKS-optimized Bottlerocket (arm64 NVIDIA) AMI"
            ami_variants[f"/aws/service/bottlerocket/aws-k8s-{k8s_version}-nvidia/x86_64"] = "Amazon EKS-optimized Bottlerocket (x86_64 NVIDIA) AMI"
    else:
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
                del item["Name"]
                del item["Type"]
                if "{" in item["Value"]:
                    v = item.pop("Value")
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


@cli_main.command(help="Find ECS optimized Bottlerocket AMIs")
@click.pass_context
def bottlerocket_ecs(ctx):
    region, session = ctx.obj["region"], ctx.obj["session"]
    resp = prompt_multi_selection("AMI", options=list(get_bottlerocket_ecs_meta_dict().keys()), pre_selected_options=[])
    for name in resp.get("AMIs", []):
        get_parameters(param_path=f"{name}/latest/image_id", region=region, session=session)


@cli_main.command(help="Find EKS optimized Bottlerocket AMIs")
@click.pass_context
def bottlerocket_eks(ctx):
    region, session = ctx.obj["region"], ctx.obj["session"]
    resp = prompt_multi_selection("AMI", options=list(get_eks_meta_dict(True).keys()), pre_selected_options=[])
    for name in resp.get("AMIs", []):
        get_parameters(param_path=f"{name}/latest/image_id", region=region, session=session)


@cli_main.command(help="Find EC2 Linux AMIs")
@click.pass_context
def ec2(ctx):
    region, session = ctx.obj["region"], ctx.obj["session"]
    data = get_parameters_by_path(param_path="/aws/service/ami-amazon-linux-latest", region=region, session=session)
    if data:
        resp = prompt_multi_selection("AMI", options=list(data.keys()), pre_selected_options=[])
        for arn in resp.get("AMIs", []):
            print(json.dumps(data[arn], default=str, indent=2, sort_keys=True))


@cli_main.command(help="Find ECS optimized AMIs")
@click.pass_context
def ecs(ctx):
    region, session = ctx.obj["region"], ctx.obj["session"]
    resp = prompt_multi_selection("AMI", options=list(get_ecs_meta_dict().keys()), pre_selected_options=[])
    for name in resp.get("AMIs", []):
        get_parameters(param_path=f"{name}/recommended", region=region, session=session)


@cli_main.command(help="Find EKS optimized AMIs")
@click.pass_context
def eks(ctx):
    region, session = ctx.obj["region"], ctx.obj["session"]
    resp = prompt_multi_selection("AMI", options=list(get_eks_meta_dict().keys()), pre_selected_options=[])
    for name in resp.get("AMIs", []):
        get_parameters(param_path=f"{name}/recommended", region=region, session=session)


@cli_main.command(help="Find EC2 Windows AMIs")
@click.pass_context
def windows(ctx):
    region, session = ctx.obj["region"], ctx.obj["session"]
    data = get_parameters_by_path(param_path="/aws/service/ami-windows-latest", region=region, session=session)
    if data:
        resp = prompt_multi_selection("AMI", options=list(data.keys()), pre_selected_options=[])
        for arn in resp.get("AMIs", []):
            print(json.dumps(data[arn], default=str, indent=2, sort_keys=True))


if __name__ == "__main__":
    cli_main(obj={})

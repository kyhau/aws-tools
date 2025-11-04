"""
Find AMI ID of the latest AMI
- EC2 Amazon Linux AMIs
- EC2 Windows Server AMIs
- ECS-optimized Amazon Linux AMIs
- ECS-optimized Bottlerocket AMIs
- ECS-optimized Windows Server AMIs
- EKS-optimized Amazon Linux AMIs
- EKS-optimized Bottlerocket AMIs
- EKS-optimized Windows Server AMIs
"""
import json

import click
from boto3.session import Session
from helper.selector import prompt_multi_selection

TOPIC_A = "AmazonLinux"
TOPIC_B = "Bottlerocket"
TOPIC_W = "Windows"


def _compare_version(version1: str, version2: str) -> bool:
    """Compare two version strings. Returns True if version1 >= version2."""
    return float(version1) >= float(version2)


def get_ecs_meta_dict(topic=TOPIC_A):
    if topic == TOPIC_A:
        # https://docs.aws.amazon.com/AmazonECS/latest/developerguide/retrieve-ecs-optimized_AMI.html
        return {
            "/aws/service/ecs/optimized-ami/amazon-linux-2023/recommended": "Amazon ECS-Optimized Amazon Linux 2023 (x86_64) AMI",
            "/aws/service/ecs/optimized-ami/amazon-linux-2023/arm64/recommended": "Amazon ECS-Optimized Amazon Linux 2023 (arm64) AMI",
            "/aws/service/ecs/optimized-ami/amazon-linux-2023/gpu/recommended": "Amazon ECS-Optimized Amazon Linux 2023 (GPU) AMI",
            "/aws/service/ecs/optimized-ami/amazon-linux-2023/inf/recommended": "Amazon ECS-Optimized Amazon Linux 2023 (Neuron) AMI",
            "/aws/service/ecs/optimized-ami/amazon-linux-2022/recommended": "Amazon ECS-Optimized Amazon Linux 2022 (x86_64) AMI (deprecated - use AL2023)",
            "/aws/service/ecs/optimized-ami/amazon-linux-2022/arm64/recommended": "Amazon ECS-Optimized Amazon Linux 2022 (arm64) AMI (deprecated - use AL2023)",
            "/aws/service/ecs/optimized-ami/amazon-linux-2022/gpu/recommended": "Amazon ECS-Optimized Amazon Linux 2022 (GPU) AMI (deprecated - use AL2023)",
            "/aws/service/ecs/optimized-ami/amazon-linux-2022/inf/recommended": "Amazon ECS-Optimized Amazon Linux 2022 (Neuron) AMI (deprecated - use AL2023)",
            "/aws/service/ecs/optimized-ami/amazon-linux-2/recommended": "Amazon ECS-Optimized Amazon Linux 2 (x86_64) AMI",
            "/aws/service/ecs/optimized-ami/amazon-linux-2/arm64/recommended": "Amazon ECS-Optimized Amazon Linux 2 (arm64) AMI",
            "/aws/service/ecs/optimized-ami/amazon-linux-2/gpu/recommended": "Amazon ECS-Optimized Amazon Linux 2 (GPU) AMI",
            "/aws/service/ecs/optimized-ami/amazon-linux-2/inf/recommended": "Amazon ECS-Optimized Amazon Linux 2 (Neuron) AMI",
            "/aws/service/ecs/optimized-ami/amazon-linux/recommended": "Amazon ECS-optimized Amazon Linux (x86_64) AMI deprecated as of 2021-04-15",
        }
    if topic == TOPIC_B:
        # https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-bottlerocket.html
        return {
            "/aws/service/bottlerocket/aws-ecs-1/arm64/latest": "Amazon ECS-Optimized Bottlerocket (arm64) AMI",
            "/aws/service/bottlerocket/aws-ecs-1/x86_64/latest": "Amazon ECS-Optimized Bottlerocket (x86_64) AMI",
            "/aws/service/bottlerocket/aws-ecs-1-nvidia/arm64/latest": "Amazon ECS-Optimized (NVIDIA GPU support) Bottlerocket (arm64) AMI",
            "/aws/service/bottlerocket/aws-ecs-1-nvidia/x86_64/latest": "Amazon ECS-Optimized (NVIDIA GPU support) Bottlerocket (x86_64) AMI",
        }
    if topic == TOPIC_W:
        # https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-windows-ami-versions.html
        return {
            "/aws/service/ami-windows-latest/Windows_Server-2025-English-Core-ECS_Optimized": "Amazon ECS-optimized Windows Server 2025 Core AMI",
            "/aws/service/ami-windows-latest/Windows_Server-2025-English-Full-ECS_Optimized": "Amazon ECS-optimized Windows Server 2025 Full AMI",
            "/aws/service/ami-windows-latest/Windows_Server-2022-English-Core-ECS_Optimized": "Amazon ECS-optimized Windows Server 2022 Core AMI",
            "/aws/service/ami-windows-latest/Windows_Server-2022-English-Full-ECS_Optimized": "Amazon ECS-optimized Windows Server 2022 Full AMI",
            "/aws/service/ami-windows-latest/Windows_Server-2019-English-Core-ECS_Optimized": "Amazon ECS-optimized Windows Server 2019 Core AMI",
            "/aws/service/ami-windows-latest/Windows_Server-2019-English-Full-ECS_Optimized": "Amazon ECS-optimized Windows Server 2019 Full AMI",
            "/aws/service/ami-windows-latest/Windows_Server-2016-English-Full-ECS_Optimized": "Amazon ECS-optimized Windows Server 2016 Full AMI",
        }
    raise ValueError(f"Invalid topic: {topic}. Must be one of {TOPIC_A}, {TOPIC_B}, or {TOPIC_W}")

def get_eks_meta_dict(topic=TOPIC_A):
    K8S_VERSIONS = [
        "1.34",  # Standard support
        "1.33",  # Standard support
        "1.32",  # Standard support
        "1.31",  # Standard support
        "1.30",  # Extended support
        "1.29",  # Extended support
        "1.28",  # Extended support
        "1.27",  # End of Extended Support (ended July 24, 2025)
        "1.26",  # Approaching EOL
        "1.25",  # Approaching EOL
        "1.24",  # End of support
        "1.23",  # End of support
        "1.22",  # End of support
        "1.21",  # End of support
        "1.20",  # End of support
        "1.19",  # End of support
        "1.18",  # End of support
        "1.17",  # End of support
    ]

    ami_variants = {}
    if topic == TOPIC_A:
        # https://docs.aws.amazon.com/eks/latest/userguide/retrieve-ami-id.html
        for k8s_version in K8S_VERSIONS:
            ami_variants[f"/aws/service/eks/optimized-ami/{k8s_version}/amazon-linux-2023/arm64/standard/recommended"] = "Amazon EKS-optimized Amazon Linux 2023 (AL2023) (arm64) AMI"
            ami_variants[f"/aws/service/eks/optimized-ami/{k8s_version}/amazon-linux-2023/x86_64/standard/recommended"] = "Amazon EKS-optimized Amazon Linux 2023 (AL2023) (x86_64) AMI"
            ami_variants[f"/aws/service/eks/optimized-ami/{k8s_version}/amazon-linux-2023/x86_64/neuron/recommended"] = "Amazon EKS-optimized Amazon Linux 2023 (AL2023) AWS Neuron (x86_64) AMI"
            ami_variants[f"/aws/service/eks/optimized-ami/{k8s_version}/amazon-linux-2023/x86_64/nvidia/recommended"] = "Amazon EKS-optimized Amazon Linux 2023 (AL2023) NVIDIA (x86_64) AMI"
            ami_variants[f"/aws/service/eks/optimized-ami/{k8s_version}/amazon-linux-2/recommended"] = "Amazon EKS-optimized Amazon Linux 2 (x86_64) AMI"
            ami_variants[f"/aws/service/eks/optimized-ami/{k8s_version}/amazon-linux-2-arm64/recommended"] = "Amazon EKS-optimized Amazon Linux 2 (arm64) AMI"
            ami_variants[f"/aws/service/eks/optimized-ami/{k8s_version}/amazon-linux-2-gpu/recommended"] = "Amazon EKS-optimized Amazon Linux 2 (GPU) AMI"
    elif topic == TOPIC_B:
        # https://docs.aws.amazon.com/eks/latest/userguide/retrieve-ami-id-bottlerocket.html
        for k8s_version in K8S_VERSIONS:
            ami_variants[f"/aws/service/bottlerocket/aws-k8s-{k8s_version}/arm64/latest"] = "Amazon EKS-optimized Bottlerocket (arm64 Standard) AMI"
            ami_variants[f"/aws/service/bottlerocket/aws-k8s-{k8s_version}/x86_64/latest"] = "Amazon EKS-optimized Bottlerocket (x86_64 Standard) AMI"
            ami_variants[f"/aws/service/bottlerocket/aws-k8s-{k8s_version}-nvidia/arm64/latest"] = "Amazon EKS-optimized Bottlerocket (arm64 NVIDIA) AMI"
            ami_variants[f"/aws/service/bottlerocket/aws-k8s-{k8s_version}-nvidia/x86_64/latest"] = "Amazon EKS-optimized Bottlerocket (x86_64 NVIDIA) AMI"
    elif topic == TOPIC_W:
        # https://docs.aws.amazon.com/eks/latest/userguide/retrieve-windows-ami-id.html
        for k8s_version in K8S_VERSIONS:
            if _compare_version(k8s_version, "1.30"):
                # Windows Server 2025 support started with EKS 1.30+
                ami_variants[f"/aws/service/ami-windows-latest/Windows_Server-2025-English-Core-EKS_Optimized-{k8s_version}"] = "Amazon EKS-optimized Windows Server 2025 Core AMI"
                ami_variants[f"/aws/service/ami-windows-latest/Windows_Server-2025-English-Full-EKS_Optimized-{k8s_version}"] = "Amazon EKS-optimized Windows Server 2025 Full AMI"
            elif _compare_version(k8s_version, "1.24"):
                ami_variants[f"/aws/service/ami-windows-latest/Windows_Server-2022-English-Core-EKS_Optimized-{k8s_version}"] = "Amazon EKS-optimized Windows Server 2022 Core AMI"
                ami_variants[f"/aws/service/ami-windows-latest/Windows_Server-2022-English-Full-EKS_Optimized-{k8s_version}"] = "Amazon EKS-optimized Windows Server 2022 Full AMI"
            ami_variants[f"/aws/service/ami-windows-latest/Windows_Server-2019-English-Core-EKS_Optimized-{k8s_version}"] = "Amazon EKS-optimized Windows Server 2019 Core AMI"
            ami_variants[f"/aws/service/ami-windows-latest/Windows_Server-2019-English-Full-EKS_Optimized-{k8s_version}"] = "Amazon EKS-optimized Windows Server 2019 Full AMI"

    return ami_variants


def get_parameters_by_path(param_path, region, session):
    params = {}
    for target_region in session.get_available_regions("ssm") if region == "all" else [region]:
        try:
            client = session.client("ssm", region_name=target_region)
            for page in client.get_paginator("get_parameters_by_path").paginate(Path=param_path):
                for p in page["Parameters"]:
                    params[p["ARN"]] = p
        except Exception as e:
            print(f"Skip region {target_region} due to error: {type(e).__name__}")
    return params


def get_parameters(param_path, region, session):
    for target_region in session.get_available_regions("ssm") if region == "all" else [region]:
        try:
            client = session.client("ssm", region_name=target_region)
            for item in client.get_parameters(Names=[param_path])["Parameters"]:
                del item["Name"]
                del item["Type"]
                if "{" in item["Value"]:
                    v = item.pop("Value")
                    item.update(json.loads(v))
                print(json.dumps(item, default=str, indent=2, sort_keys=True))
        except Exception as e:
            print(f"Skip region {target_region} due to error: {type(e).__name__}")


def get_amis_from_get_parameters_by_path(param_path, region, session):
    data = get_parameters_by_path(param_path=param_path, region=region, session=session)
    if data:
        amis = prompt_multi_selection("AMI", options=list(data.keys()), pre_selected_options=[])
        for arn in amis:
            print(json.dumps(data[arn], default=str, indent=2, sort_keys=True))


def get_amis_from_get_parameters(ami_dict, region, session):
    amis = prompt_multi_selection("AMI", options=list(ami_dict.keys()), pre_selected_options=[])
    for name in amis:
        get_parameters(param_path=f"{name}/image_id", region=region, session=session)


@click.group(help="List the latest AWS managed AMIs")
@click.option("--profile", "-p", default="default", show_default=True, help="AWS profile name")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS region, or 'all' for all regions")
@click.pass_context
def cli_main(ctx, profile, region):
    session = Session(profile_name=profile)
    ctx.obj = {"session": session, "region": region}


@cli_main.command(help="Find Amazon EC2 Amazon Linux AMIs")
@click.pass_context
def ec2_amazon_linux(ctx):
    # https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-ami-versions.html
    get_amis_from_get_parameters_by_path("/aws/service/ami-amazon-linux-latest", ctx.obj["region"], ctx.obj["session"])


@cli_main.command(help="Find Amazon EC2 Windows Server AMIs")
@click.pass_context
def ec2_windows(ctx):
    # https://docs.aws.amazon.com/AWSEC2/latest/WindowsGuide/finding-an-ami.html#finding-an-ami-aws-cli
    get_amis_from_get_parameters_by_path("/aws/service/ami-windows-latest", ctx.obj["region"], ctx.obj["session"])


@cli_main.command(help="Find Amazon ECS-optimized Amazon Linux AMIs")
@click.pass_context
def ecs_amazon_linux(ctx):
    get_amis_from_get_parameters(get_ecs_meta_dict(TOPIC_A), ctx.obj["region"], ctx.obj["session"])


@cli_main.command(help="Find Amazon ECS-optimized Bottlerocket AMIs")
@click.pass_context
def ecs_bottlerocket(ctx):
    get_amis_from_get_parameters(get_ecs_meta_dict(TOPIC_B), ctx.obj["region"], ctx.obj["session"])


@cli_main.command(help="Find Amazon ECS-optimized Windows Server AMIs")
@click.pass_context
def ecs_windows(ctx):
    get_amis_from_get_parameters(get_ecs_meta_dict(TOPIC_W), ctx.obj["region"], ctx.obj["session"])


@cli_main.command(help="Find Amazon EKS-optimized Amazon Linux AMIs")
@click.pass_context
def eks_amazon_linux(ctx):
    get_amis_from_get_parameters(get_eks_meta_dict(TOPIC_A), ctx.obj["region"], ctx.obj["session"])


@cli_main.command(help="Find Amazon EKS-optimized Bottlerocket AMIs")
@click.pass_context
def eks_bottlerocket(ctx):
    get_amis_from_get_parameters(get_eks_meta_dict(TOPIC_B), ctx.obj["region"], ctx.obj["session"])


@cli_main.command(help="Find Amazon EKS-optimized Windows AMIs")
@click.pass_context
def eks_windows(ctx):
    get_amis_from_get_parameters(get_eks_meta_dict(TOPIC_W), ctx.obj["region"], ctx.obj["session"])


if __name__ == "__main__":
    cli_main(obj={})

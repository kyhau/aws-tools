"""
bash:
aws ssm get-parameters "$@" --names /aws/service/ecs/optimized-ami/amazon-linux-2/recommended/image_id --query "Parameters[0].Value" --output text
aws ssm get-parameters "$@" --names /aws/service/eks/optimized-ami/1.14/amazon-linux-2/recommended/image_id --query "Parameters[0].Value" --output text
"""
from boto3.session import Session
import click
import json
import yaml


def process(param_path, region, session):
    for region in session.get_available_regions("ssm") if region == "all" else [region]:
        try:
            client = session.client("ssm", region_name=region)
            for item in client.get_parameters(Names=[param_path])["Parameters"]:
                v = item.pop("Value")
                del item["Name"]
                del item["Type"]
                item.update(json.loads(v))
                print(yaml.dump(item))
        except Exception as e:
            print(f"Skip region {region} due to error: {e}")


@click.group(help="List the latest AWS managed AMIs")
@click.option("--profile", "-p", default="default", show_default=True, help="AWS profile name")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS region")
@click.pass_context
def cli_main(ctx, profile, region):
    session = Session(profile_name=profile)
    ctx.obj = {"session": session, "region": region}


@cli_main.command(help="Print the latest ECS Optimized Amazon Linux 2 AMIs")
@click.pass_context
def ecs(ctx):
    region, session = ctx.obj["region"], ctx.obj["session"]
    process(param_path="/aws/service/ecs/optimized-ami/amazon-linux-2/recommended", region=region, session=session)


@cli_main.command(help="Print the latest EKS Optimized Amazon Linux 2 AMIs")
@click.pass_context
def eks(ctx):
    region, session = ctx.obj["region"], ctx.obj["session"]
    process(param_path="/aws/service/eks/optimized-ami/1.14/amazon-linux-2/recommended", region=region, session=session)


if __name__ == "__main__":
    cli_main(obj={})

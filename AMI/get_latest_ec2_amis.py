"""
bash:
aws ssm get-parameters-by-path --path "/aws/service/ami-amazon-linux-latest" | jq '.Parameters[] | "\(.Value) \(.Version) \(.ARN)"'
aws ssm get-parameters-by-path --path "/aws/service/ami-windows-latest" | jq '.Parameters[] | "\(.Value) \(.Version) \(.ARN)"'
"""
from boto3.session import Session
import click


def process(param_path, region, session):
    for region in session.get_available_regions("ssm") if region == "all" else [region]:
        try:
            client = session.client("ssm", region_name=region)
            for page in client.get_paginator("get_parameters_by_path").paginate(Path=param_path):
                for p in page["Parameters"]:
                    print(f'{p["Value"]}, {p["Version"]}, {p["LastModifiedDate"]}, {p["ARN"]}')
        except Exception as e:
            print(f"Skip region {region} due to error: {e}")


@click.group(help="List the lastest AWS managed AMIs")
@click.option("--profile", "-p", default="default", show_default=True, help="AWS profile name")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS region")
@click.pass_context
def cli_main(ctx, profile, region):
    session = Session(profile_name=profile)
    ctx.obj = {"session": session, "region": region}
    print("AmiId, Version, LastModifiedDate, ARN")


@cli_main.command(help="List all Linux AMIs")
@click.pass_context
def linux(ctx):
    """List all Linux AMIs."""
    region, session = ctx.obj["region"], ctx.obj["session"]
    process(param_path="/aws/service/ami-amazon-linux-latest", region=region, session=session)


@cli_main.command(help="List all Windows AMIs")
@click.pass_context
def windows(ctx):
    """List all Windows AMIs."""
    region, session = ctx.obj["region"], ctx.obj["session"]
    process(param_path="/aws/service/ami-windows-latest", region=region, session=session)


if __name__ == "__main__":
    cli_main(obj={})

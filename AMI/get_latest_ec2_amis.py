"""
bash:
aws ssm get-parameters-by-path --path "/aws/service/ami-amazon-linux-latest" | jq '.Parameters[] | "\(.Value) \(.Version) \(.ARN)"'
aws ssm get-parameters-by-path --path "/aws/service/ami-windows-latest" | jq '.Parameters[] | "\(.Value) \(.Version) \(.ARN)"'
"""
from boto3.session import Session
import typer

app = typer.Typer(help="List the latest AWS managed AMIs.")


def process(param_path, region):
    operation_params = {"Path": param_path}
    session = Session()
    regions = session.get_available_regions("ssm") if region == "all" else [region]
    for region in regions:
        try:
            client = session.client("ssm", region_name=region)
            paginator = client.get_paginator("get_parameters_by_path")
            for page in paginator.paginate(**operation_params):
                for p in page["Parameters"]:
                    print(f'{p["Value"]}, {p["Version"]}, {p["LastModifiedDate"]}, {p["ARN"]}')
        except Exception as e:
            print(f"Skip region {region} due to error: {e}")


@app.command()
def linux_amis(
    region: str = typer.Option("ap-southeast-2", help="AWS Region; use 'all' for all regions.", show_default=True)
):
    """List all Linux AMIs."""
    process(param_path="/aws/service/ami-amazon-linux-latest", region=region)


@app.command()
def windows_amis(
    region: str = typer.Option("ap-southeast-2", help="AWS Region; use 'all' for all regions.", show_default=True)
):
    """List all Windows AMIs."""
    process(param_path="/aws/service/ami-windows-latest", region=region)


if __name__ == "__main__":
    app()

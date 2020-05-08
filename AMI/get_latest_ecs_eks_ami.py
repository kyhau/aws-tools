"""
bash:
aws ssm get-parameters "$@" --names /aws/service/ecs/optimized-ami/amazon-linux-2/recommended/image_id --query "Parameters[0].Value" --output text
aws ssm get-parameters "$@" --names /aws/service/eks/optimized-ami/1.14/amazon-linux-2/recommended/image_id --query "Parameters[0].Value" --output text
"""
from boto3.session import Session
import json
import typer
import yaml

app = typer.Typer(help="List the latest AWS managed AMIs.")


def process(param_path, region):
    operation_params = {"Names": [param_path]}
    session = Session()
    regions = session.get_available_regions("ssm") if region == "all" else [region]
    for region in regions:
        try:
            client = session.client("ssm", region_name=region)
            for item in client.get_parameters(**operation_params)["Parameters"]:
                v = item.pop("Value")
                del item["Name"]
                del item["Type"]
                item.update(json.loads(v))
                print(yaml.dump(item))
        except Exception as e:
            print(f"Skip region {region} due to error: {e}")


@app.command()
def ecs_optimized_ami(
    region: str = typer.Option("ap-southeast-2", help="AWS Region; use 'all' for all regions.", show_default=True)
):
    """Print the latest ECS Optimised Amazon Linux 2 AMI."""
    process(param_path="/aws/service/ecs/optimized-ami/amazon-linux-2/recommended", region=region)


@app.command()
def eks_optimized_ami(
    region: str = typer.Option("ap-southeast-2", help="AWS Region; use 'all' for all regions.", show_default=True)
):
    """Print the latest EKS Optimised Amazon Linux 2 AMI."""
    process(param_path="/aws/service/eks/optimized-ami/1.14/amazon-linux-2/recommended", region=region)


if __name__ == "__main__":
    app()

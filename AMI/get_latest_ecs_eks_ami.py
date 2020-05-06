"""
bash:
aws ssm get-parameters "$@" --names /aws/service/ecs/optimized-ami/amazon-linux-2/recommended/image_id --query "Parameters[0].Value" --output text
aws ssm get-parameters "$@" --names /aws/service/eks/optimized-ami/1.14/amazon-linux-2/recommended/image_id --query "Parameters[0].Value" --output text
"""
from boto3.session import Session
import click
import yaml


@click.command()
@click.option("--latest-ecs-optimized-ami", "-c", is_flag=True, help="Print the latest ECS Optimised Amazon Linux 2 AMI.")
@click.option("--latest-eks-optimized-ami", "-k", is_flag=True, help="Print the latest EKS Optimised Amazon Linux 2 AMI.")
@click.option("--region", "-r", help="AWS Region; use 'all' for all regions; default ap-southeast-2.", default="ap-southeast-2")
def main(latest_ecs_optimized_ami, latest_eks_optimized_ami, region):
    session = Session()
    regions = session.get_available_regions("ssm") if region == "all" else [region]

    operation_params = {"Names": ["/aws/service/ecs/optimized-ami/amazon-linux-2/recommended"]}
    if latest_eks_optimized_ami is True:
        operation_params["Names"] = ["/aws/service/eks/optimized-ami/1.14/amazon-linux-2/recommended"]

    for region in regions:
        try:
            client = session.client("ssm", region_name=region)
            import json
            for item in client.get_parameters(**operation_params)["Parameters"]:
                v = item.pop("Value")
                del item["Name"]
                del item["Type"]
                item.update(json.loads(v))
                print(yaml.dump(item))
        except Exception as e:
            print(f"Skip region {region} due to error: {e}")


if __name__ == "__main__": main()

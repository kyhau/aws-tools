"""
bash:
aws ssm get-parameters-by-path --path "/aws/service/ami-amazon-linux-latest" | jq '.Parameters[] | "\(.Value) \(.Version) \(.ARN)"'
aws ssm get-parameters-by-path --path "/aws/service/ami-windows-latest" | jq '.Parameters[] | "\(.Value) \(.Version) \(.ARN)"'
"""
from boto3.session import Session
import click


@click.command()
@click.option("--list-linux-amis", "-l", is_flag=True, help="List all Linux AMIs.")
@click.option("--list-windows-amis", "-w", is_flag=True, help="List all Windows AMIs.")
@click.option("--region", "-r", help="AWS Region; use 'all' for all regions; default ap-southeast-2.", default="ap-southeast-2")
def main(list_linux_amis, list_windows_amis, region):
    operation_params = {
        "Path": f"/aws/service/{'ami-windows-latest' if list_windows_amis is True else 'ami-amazon-linux-latest'}"
    }

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


if __name__ == "__main__": main()

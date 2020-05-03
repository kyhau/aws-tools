from boto3.session import Session
from botocore.exceptions import ClientError
import click
from configparser import ConfigParser
import logging
from os.path import expanduser, join
import yaml

logging.getLogger().setLevel(logging.DEBUG)

aws_profiles = []
try:
    cp = ConfigParser()
    cp.read(join(expanduser("~"), ".aws", "credentials"))
    aws_profiles = cp.sections()
except Exception as e:
    logging.error(e)


def process_account(session, profile, account_id, aws_region, vpn_connection_id):
    operation_params = { "VpnConnectionIds": [vpn_connection_id] } if vpn_connection_id else {}

    regions = session.get_available_regions("ec2") if aws_region == "all" else [aws_region]
    for region in regions:
        logging.debug(f"Checking {account_id} {profile} {region}")
        try:
            client = session.client("ec2", region_name=region)
            items = client.describe_vpn_connections(**operation_params)["VpnConnections"]
            for item in items:
                print("--------------------------------------------------------------------------------")
                print(yaml.dump(item))
            if items and vpn_connection_id:
                return True

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code in ["AuthFailure", "UnrecognizedClientException"]:
                logging.warning(f"Unable to process region {region}: {error_code}")
            else:
                raise
        except Exception:
            import traceback
            traceback.print_exc()


@click.command()
@click.option("--profile", "-p", help="AWS profile name")
@click.option("--vpcconnectionid", "-v", help="VPN Connection ID. Default: Describes all your VPC connections.", default=None)
@click.option("--region", "-r", help="AWS Region; use 'all' for all regions", default="ap-southeast-2")
def main(profile, vpcconnectionid, region):
    accounts_processed = []
    profile_names = [profile] if profile else aws_profiles
    for profile_name in profile_names:
        try:
            session = Session(profile_name=profile_name)
            account_id = session.client("sts").get_caller_identity()["Account"]
            if account_id in accounts_processed:
                continue
            accounts_processed.append(account_id)
            
            if process_account(session, profile_name, account_id, region, vpcconnectionid) is not None:
                break
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code in ["ExpiredToken", "AccessDenied"]:
                logging.warning(f"{profile_name} {error_code}. Skipped")
            else:
                raise


if __name__ == "__main__": main()

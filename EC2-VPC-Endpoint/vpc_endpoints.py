"""
A helper script to call describe_vpc_endpoints as well as lookup ENI IPs.
"""
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


def new_operation_params(endpoint_id, service_name, vpc_id):
    operation_params = {"Filters": []}
    if endpoint_id:
        operation_params["VpcEndpointIds"] = [endpoint_id]
    if service_name:
        operation_params["Filters"].append({"Name": "service-name", "Values": [service_name]})
    if vpc_id:
        operation_params["Filters"].append({"Name": "vpc-id", "Values": [vpc_id]})
    return operation_params


def process_region(client, operation_params, endpoint_type):
    cnt = 0
    paginator = client.get_paginator("describe_vpc_endpoints")
    for page in paginator.paginate(**operation_params):
        for item in page["VpcEndpoints"]:
            if endpoint_type and endpoint_type != item["VpcEndpointType"].lower():
                continue
            
            if item["NetworkInterfaceIds"]:
                # Retrieve also the primary private IPs for the ENIs
                resp2 = client.describe_network_interfaces(NetworkInterfaceIds=item["NetworkInterfaceIds"])
                eni_data = [
                    f'{item2["NetworkInterfaceId"]}, {item2["PrivateIpAddress"]}' for item2 in resp2["NetworkInterfaces"]
                ]
                item["NetworkInterfaceIds"] = eni_data
            
            print(yaml.dump(item))
            print("--------------------------------------------------------------------------------")
            cnt += 1
    logging.debug(f"Total items: {cnt}")


def process_account(session, profile, aws_region, operation_params, endpoint_type):
    regions = session.get_available_regions("ec2") if aws_region == "all" else [aws_region]
    for region in regions:
        logging.debug(f"Checking {profile} {region}")
        try:
            client = session.client("ec2", region_name=region)
            process_region(client, operation_params, endpoint_type)
        
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code in ["AuthFailure", "UnrecognizedClientException"]:
                logging.warning(f"Unable to process region {region}: {error_code}")
            else:
                raise
        except Exception:
            import traceback
            traceback.print_exc()


################################################################################
# Entry point

@click.command()
@click.option("--profile", "-p", help="AWS profile name.")
@click.option("--region", "-r", help="AWS Region; use 'all' for all regions.", default="ap-southeast-2")
@click.option("--endpointid", "-e", help="VPC endpoint ID. Optional. E.g. vpce-123456789012")
@click.option("--endpointtype", "-t", help="VPC endpoint type (Gateway|Interface). Return all if not specified.")
@click.option("--servicename", "-s", help="Service name. Optional. E.g. com.amazonaws.ap-southeast-2.s3")
@click.option("--vpcid", "-v", help="VPC ID. Optional. E.g. vpc-123456789012")
def main(profile, region, endpointid, endpointtype, servicename, vpcid):
    accounts_processed = []
    profile_names = [profile] if profile else aws_profiles

    operation_params = new_operation_params(endpointid, servicename, vpcid)
    endpointtype = endpointtype if endpointtype is None else endpointtype.lower()
    
    for profile_name in profile_names:
        try:
            session = Session(profile_name=profile_name)
            account_id = session.client("sts").get_caller_identity()["Account"]
            if account_id in accounts_processed:
                continue
            accounts_processed.append(account_id)
            
            process_account(session, profile_name, region, operation_params, endpointtype)
        
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code in ["ExpiredToken", "InvalidClientTokenId", "AccessDeniedException"]:
                logging.warning(f'{profile_name} {error_code}. Skipped')
            else:
                raise


if __name__ == "__main__": main()

"""
A helper script to call describe_vpc_endpoint_services.
"""
from boto3.session import Session
from botocore.exceptions import ClientError
import click
import logging
from time import time
import yaml

# Update the root logger to get messages at DEBUG and above
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger("botocore").setLevel(logging.CRITICAL)
logging.getLogger("boto3").setLevel(logging.CRITICAL)
logging.getLogger("urllib3.connectionpool").setLevel(logging.CRITICAL)


def read_aws_profile_names():
    from configparser import ConfigParser
    from os.path import expanduser, join
    try:
        cp = ConfigParser()
        cp.read(join(expanduser("~"), ".aws", "credentials"))
        return cp.sections()
    except Exception as e:
        logging.error(e)


def new_operation_params(service_name):
    return {"ServiceNames": [service_name]} if service_name else {}


def match_service_type(item, target_service_type):
    if target_service_type is None:
        return True

    for subitem in item["ServiceType"]:
        curr = subitem.get("ServiceType")
        if curr is not None and curr.lower() == target_service_type:
            return True
    return False


def process_region(client, operation_params, endpoint_type, name_only):
    cnt = 0
    paginator = client.get_paginator("describe_vpc_endpoint_services")
    for page in paginator.paginate(**operation_params):
        for item in page["ServiceDetails"]:
            if match_service_type(item, endpoint_type):
                if name_only:
                    print(item["ServiceName"])
                else:
                    print(yaml.dump(item))
                    print("--------------------------------------------------------------------------------")
                cnt += 1
    logging.debug(f"Total items: {cnt}")


def process_account(session, profile, aws_region, operation_params, endpoint_type, name_only):
    regions = session.get_available_regions("ec2") if aws_region == "all" else [aws_region]
    for region in regions:
        logging.debug(f"Checking {profile} {region}")
        try:
            client = session.client("ec2", region_name=region)
            process_region(client, operation_params, endpoint_type, name_only)
        
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code in ["AccessDenied", "AccessDeniedException", "AuthFailure", "UnrecognizedClientException"]:
                logging.warning(f"Unable to process region {region}: {error_code}")
            else:
                raise
        except Exception:
            import traceback
            traceback.print_exc()


@click.command()
@click.option("--endpointtype", "-t", help="VPC endpoint type (Gateway|Interface). Return all if not specified.")
@click.option("--nameonly", "-n", is_flag=True, help="Show names only")
@click.option("--servicename", "-s", help="Service name. Optional. E.g. com.amazonaws.ap-southeast-2.s3")
@click.option("--profile", "-p", help="AWS profile name.")
@click.option("--region", "-r", help="AWS Region; use 'all' for all regions.", default="ap-southeast-2")
def main(endpointtype, nameonly, servicename, profile, region):
    start = time()
    try:
        accounts_processed = []

        operation_params = new_operation_params(servicename)
        endpointtype = endpointtype if endpointtype is None else endpointtype.lower()

        profile_names = [profile] if profile else read_aws_profile_names()
        for profile_name in profile_names:
            try:
                session = Session(profile_name=profile_name)
                account_id = session.client("sts").get_caller_identity()["Account"]
                if account_id in accounts_processed:
                    continue
                accounts_processed.append(account_id)

                process_account(session, profile_name, region, operation_params, endpointtype, nameonly)
            except ClientError as e:
                error_code = e.response["Error"]["Code"]
                if error_code in ["ExpiredToken", "InvalidClientTokenId"]:
                    logging.warning(f"{profile_name} {error_code}. Skipped")
                else:
                    raise
    finally:
        logging.info(f"Total execution time: {time() - start}s")


if __name__ == "__main__":
    main()

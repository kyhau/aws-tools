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


def new_operation_params(group_id):    
    operation_params = {}
    if group_id:
        operation_params["GroupIds"] = [group_id]
    
    # Do not use "GroupNames"
    # --group-names option is applied ONLY to the default VPC, and otherwise you have to use the filters to query
    return operation_params


def process_region(client, operation_params, group_name):
    paginator = client.get_paginator("describe_security_groups")
    cnt = 0
    group_name = group_name.lower() if group_name else group_name
    for page in paginator.paginate(**operation_params):
        for item in page["SecurityGroups"]:
            if group_name is None or item["GroupName"].lower() == group_name:
                print("--------------------------------------------------------------------------------")
                print(yaml.dump(item))
                cnt += 1
    print(f"Total: {cnt}")
    return cnt


def process_account(session, profile, account_id, aws_region, group_id, group_name):
    operation_params = new_operation_params(group_id)

    regions = session.get_available_regions("ec2") if aws_region == "all" else [aws_region]
    for region in regions:
        logging.debug(f"Checking {account_id} {profile} {region}")
        try:
            client = session.client("ec2", region_name=region)
            cnt = process_region(client, operation_params, group_name)
            if cnt and (group_id or group_name):
                return cnt

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
@click.option("--groupid", "-i", help="ID of the Security Group. Default: Describes all your security groups.", default=None)
@click.option("--groupname", "-n", help="Name of the Security Group. Default: Describes all your security groups.", default=None)
@click.option("--profile", "-p", help="AWS profile name")
@click.option("--region", "-r", help="AWS Region; use 'all' for all regions", default="ap-southeast-2")
def main(groupid, groupname, profile, region):
    start = time()
    try:
        accounts_processed = []
        profile_names = [profile] if profile else read_aws_profile_names()
        for profile_name in profile_names:
            try:
                session = Session(profile_name=profile_name)
                account_id = session.client("sts").get_caller_identity()["Account"]
                if account_id in accounts_processed:
                    continue
                accounts_processed.append(account_id)

                if process_account(session, profile_name, account_id, region, groupid, groupname) is not None:
                    break
            except ClientError as e:
                error_code = e.response["Error"]["Code"]
                if error_code in ["AccessDenied", "ExpiredToken"]:
                    logging.warning(f"{profile_name} {error_code}. Skipped")
                else:
                    raise
    finally:
        logging.info(f"Total execution time: {time() - start}s")


if __name__ == "__main__":
    main()

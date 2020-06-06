"""
Identify databases hosted in EC2 instances, by inspecting security groups for common database ports.
"""
from boto3.session import Session
from botocore.exceptions import ClientError
import click
import logging
from time import time

# Update the root logger to get messages at DEBUG and above
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger("botocore").setLevel(logging.CRITICAL)
logging.getLogger("boto3").setLevel(logging.CRITICAL)
logging.getLogger("urllib3.connectionpool").setLevel(logging.CRITICAL)

common_db_server_ports = [
    1433,   # MS SQL Server
    3306,   # MySQL
    5432,   # PostgreSQL
    49000,  # Informix
]


def read_aws_profile_names():
    from configparser import ConfigParser
    from os.path import expanduser, join
    try:
        cp = ConfigParser()
        cp.read(join(expanduser("~"), ".aws", "credentials"))
        return cp.sections()
    except Exception as e:
        logging.error(e)


def subnet_names(client, subnet_ids):
    ret = {}
    for subnet in client.describe_subnets(SubnetIds=subnet_ids)["Subnets"]:
        if "Tags" in subnet:
            name = None
            for tag in subnet["Tags"]:
                if tag["Key"] == "Name":
                    name = tag["Value"]
            if name is not None:
                ret[subnet["SubnetId"]] = name
    return ret


def process_data(response, account_id, region, profile, session):
    for sg in response["SecurityGroups"]:
        ports_matched = {i.get("FromPort") for i in sg["IpPermissions"] if i.get("FromPort") in common_db_server_ports}
        if ports_matched:
            client = session.client("ec2", region_name=region)
            ret = client.describe_network_interfaces(Filters=[{"Name": "group-id", "Values": [sg["GroupId"]]}])

            instance_id_subnet_set = {
                (r["Attachment"]["InstanceId"], r["SubnetId"])
                for r in ret["NetworkInterfaces"]
                if "Attachment" in r and "InstanceId" in r["Attachment"]
            }

            if instance_id_subnet_set:
                subnet_ids = {y for (x, y) in instance_id_subnet_set}
    
                subnet_id_dict_data = subnet_names(client, list(subnet_ids))
    
                for (instance_id, subnet_id) in instance_id_subnet_set:
                    data = [
                        account_id,
                        region,
                        profile,
                        sg["GroupId"],
                        "|".join(map(str, ports_matched)),
                        instance_id,
                        subnet_id_dict_data[subnet_id],  # subnet name
                    ]
                    print(",".join(data))


def process_account(session, profile, account_id, aws_region, group_id):
    regions = session.get_available_regions("ec2") if aws_region == "all" else [aws_region]
    for region in regions:
        logging.debug(f"Checking {account_id} {region}")
        try:
            client = session.client("ec2", region_name=region)
            
            if group_id is None:
                paginator = client.get_paginator("describe_security_groups")
                for page in paginator.paginate():
                    process_data(page, account_id, region, profile, session)
            else:
                ret = client.describe_security_groups(GroupIds=[group_id])
                process_data(ret, account_id, region, profile, session)
                return ret

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code in [
                "AccessDenied", "AuthFailure", "UnrecognizedClientException", "UnauthorizedOperation", "RequestExpired"
            ]:
                logging.warning(f"Unable to process region {region}: {error_code}")
            else:
                raise
        except Exception:
            import traceback
            traceback.print_exc()


@click.command()
@click.option("--groupid", "-i", help="Security Group ID", default=None)
@click.option("--profile", "-p", help="AWS profile name")
@click.option("--region", "-r", help="AWS Region; use 'all' for all regions", default="ap-southeast-2")
def main(groupid, profile, region):
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

                if process_account(session, profile_name, account_id, region, groupid) is not None:
                    break
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

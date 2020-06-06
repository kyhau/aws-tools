"""
Output: account_id, region, instance_id, private_ip, public_ip
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

amis_known = {}


def read_aws_profile_names():
    from configparser import ConfigParser
    from os.path import expanduser, join
    try:
        cp = ConfigParser()
        cp.read(join(expanduser("~"), ".aws", "credentials"))
        return cp.sections()
    except Exception as e:
        logging.error(e)


def get_tag_value(tags, key="Name"):
    for tag in tags:
        if tag["Key"] == key:
            return tag["Value"]
    return ""


def get_image(ami_id, client):
    if ami_id not in amis_known:
        try:
            image = client.describe_images(ImageIds=[ami_id])["Images"][0]
            amis_known[ami_id] = [
                image.get("Name", "NoName"),
                "Public" if image["Public"] is True else "Private",
            ]
        except:
            amis_known[ami_id] = ["NoAMIName", "UnknownAMI"]
    return amis_known[ami_id]


def process_data(response, account_id, region, profile, client, detailed):
    for item in response["Reservations"]:
        for i in item["Instances"]:
            data = [
                account_id,
                region,
                profile,
                i["InstanceId"],
                get_tag_value(i["Tags"]),
                i.get("Platform", "Linux/UNIX"),
                i.get("PrivateIpAddress"),
                i.get("PublicIpAddress", "NoPublicIP"),
            ]
            if detailed:
                data += get_image(i["ImageId"], client)
            print(",".join(data))


def process_account(session, profile, account_id, aws_region, instance_id, detailed):
    regions = session.get_available_regions("ec2") if aws_region == "all" else [aws_region]
    for region in regions:
        logging.debug(f"Checking {account_id} {profile} {region}")
        try:
            client = session.client("ec2", region_name=region)
            if instance_id is None:
                paginator = client.get_paginator("describe_instances")
                for page in paginator.paginate():
                    process_data(page, account_id, region, profile, client, detailed)
            else:
                ret = client.describe_instances(InstanceIds=[instance_id])
                process_data(ret, account_id, region, profile, client, detailed)
                return ret

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code in ["AccessDenied", "AuthFailure", "UnrecognizedClientException"]:
                logging.warning(f"Unable to process region {region}: {error_code}")
            elif error_code == "InvalidInstanceID.NotFound":
                pass
            else:
                raise
        except Exception:
            import traceback
            traceback.print_exc()


@click.command()
@click.option("--profile", "-p", help="AWS profile name")
@click.option("--instanceid", "-i", help="EC2 instance ID", default=None)
@click.option("--region", "-r", help="AWS Region; use 'all' for all regions", default="ap-southeast-2")
@click.option("--detailed", "-d", is_flag=True)
def main(profile, instanceid, region, detailed):
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

                if process_account(session, profile_name, account_id, region, instanceid, detailed) is not None:
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

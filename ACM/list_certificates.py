"""
List certificates of account(s)
"""
from boto3.session import Session
from botocore.exceptions import ClientError
import click
from datetime import date, datetime
import json
import logging
from time import time

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


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def process_account(session, account_id, aws_region, detailed):
    regions = session.get_available_regions("acm") if aws_region == "all" else [aws_region]
    for region in regions:
        logging.debug(f"Checking {account_id} {region}")
        try:
            client = session.client("acm", region_name=region)
            data_list = []
            for page in client.get_paginator("list_certificates").paginate():
                data_list.extend(page["CertificateSummaryList"])
            
            for data in data_list:
                item = client.describe_certificate(CertificateArn=data["CertificateArn"])["Certificate"]
                
                data = item if detailed else {
                    "AccountId": account_id,
                    "Region": region,
                    "CertificateArn": item["CertificateArn"],
                    "DomainName": item["DomainName"],
                    "NotAfter": item["NotAfter"].strftime("%Y-%m-%d %H:%M:%S"),
                    "InUseByCnt": len(item["InUseBy"]),
                    "Issuer": item["Issuer"],
                    "Status": item["Status"],
                    "Type": item["Type"],
                }
                print(json.dumps(data, indent=2, sort_keys=True, default=json_serial))

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code in ["AccessDeniedException", "AuthFailure", "UnrecognizedClientException"]:
                logging.warning(f"Unable to process region {region}: {error_code}")
            else:
                raise
        except Exception:
            import traceback
            traceback.print_exc()


@click.command()
@click.option("--detailed", "-d", show_default=True, is_flag=True)
@click.option("--profile", "-p", help="AWS profile name.")
@click.option("--region", "-r", help="AWS Region; use 'all' for all regions.", default="ap-southeast-2")
def main(detailed, profile, region):
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
        
                process_account(session, account_id, region, detailed)
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

from boto3.session import Session
from botocore.exceptions import ClientError
import click
from configparser import ConfigParser
from datetime import date, datetime
import json
import logging
from os.path import expanduser, join

# Update the root logger to get messages at DEBUG and above
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger("botocore").setLevel(logging.CRITICAL)
logging.getLogger("boto3").setLevel(logging.CRITICAL)
logging.getLogger("urllib3").setLevel(logging.CRITICAL)

aws_profiles = []
try:
    cp = ConfigParser()
    cp.read(join(expanduser("~"), ".aws", "credentials"))
    aws_profiles = cp.sections()
except Exception as e:
    logging.error(e)


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))


def process_account(session, account_id, aws_region):
    regions = session.get_available_regions("acm") if aws_region == "all" else [aws_region]
    for region in regions:
        logging.debug(f"Checking {account_id} {region}")
        try:
            client = session.client("acm", region_name=region)
            data_list = []
            
            paginator = client.get_paginator("list_certificates")
            for page in paginator.paginate():
                data_list.extend(page["CertificateSummaryList"])
            
            for data in data_list:
                ret = client.describe_certificate(CertificateArn=data["CertificateArn"])
                print(json.dumps(ret["Certificate"], indent=2, sort_keys=True, default=json_serial))

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code in ["AuthFailure", "UnrecognizedClientException"]:
                logging.warning(f"Unable to process region {region}: {error_code}")
            else:
                raise
        except Exception as e:
            logging.error(e)
            import traceback
            traceback.print_exc()


################################################################################
# Entry point

@click.command()
@click.option("--profile", "-p", help="AWS profile name.")
@click.option("--region", "-r", help="AWS Region; use 'all' for all regions.", default="ap-southeast-2")
def main(profile, region):
    accounts_processed = []
    profile_names = [profile] if profile else aws_profiles
    
    for profile_name in profile_names:
        try:
            session = Session(profile_name=profile_name)
            account_id = session.client("sts").get_caller_identity()["Account"]
            if account_id in accounts_processed:
                continue
            accounts_processed.append(account_id)
            
            process_account(session, account_id, region)

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "ExpiredToken":
                logging.warning(f'{profile_name} {error_code}. Skipped')
            else:
                raise


if __name__ == "__main__": main()

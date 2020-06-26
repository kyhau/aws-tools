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

TARGETS = [
    "Auto Scaling Group Resources",
    "Amazon EBS Public Snapshots",
    "Amazon RDS Public Snapshots",
    "Amazon S3 Bucket Permissions",
    "CloudFront Custom SSL Certificates in the IAM Certificate Store",
    "CloudFront SSL Certificate on the Origin Server",
    "IAM Access Key Rotation",
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


def process_request(session, account_id):
    # Trusted Advisor only works in "us-east-1" or no region
    client = session.client("support", region_name="us-east-1")

    ret = []
    for item in [x for x in client.describe_trusted_advisor_checks(language="en")["checks"] if x["name"] in TARGETS]:
        result = client.describe_trusted_advisor_check_result(checkId=item["id"], language="en")["result"]
        if result["status"] in ["error", "warning"]:  
            # "ok" (green), "warning" (yellow), "error" (red), "not_available"
            data = {
                "AccountId": account_id,
                "Category": item["category"],
                "Id": item["id"],
                "Name": item["name"],
                "ResourcesFlaggedCnt": result.get("resourcesSummary", {}).get("resourcesFlagged", 0),
                "ResourcesFlagged": result.get("flaggedResources", []),
            }
            ret.append(data)
    return ret


def process_account(session, account_id):
    start, items = time(), []
    try:
        items = process_request(session, account_id)
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code in ["AccessDenied", "AccessDeniedException", "AuthFailure", "UnrecognizedClientException"]:
            logging.warning(f"Unable to process {account_id}: {error_code}")
        else:
            raise
    finally:
        logging.info(f"{account_id}, cnt={len(items)}, time={time() - start}s")
        for item in items:
            logging.info(item)


@click.command()
@click.option("--profile", "-p", help="AWS profile name")
def main(profile):
    start = time()
    try:
        accounts_processed = []
        profile_names = [profile] if profile else read_aws_profile_names()
        for profile_name in profile_names:
            session = Session(profile_name=profile_name)
            account_id = session.client("sts").get_caller_identity()["Account"]
            if account_id in accounts_processed:
                continue
            accounts_processed.append(account_id)
            process_account(session, account_id)
    finally:
        logging.info(f"Total execution time: {time() - start}s")


if __name__ == "__main__":
    main()

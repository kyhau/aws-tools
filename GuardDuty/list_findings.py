from boto3.session import Session
from botocore.exceptions import ClientError
import click
from configparser import ConfigParser
import logging
from os.path import expanduser, join
import yaml

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

accounts_processed = []

# See https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_findings.html#guardduty_findings-severity
severity_defaults = {
    "high": 7,
    "medium": 4,
    "low": 0,
}


def list_detectors(client):
    ret = []
    paginator = client.get_paginator("list_detectors")
    for page in paginator.paginate():
        l = page.get("DetectorIds")
        if l is not None:
            ret.extend(l)
    return ret


def get_finding_ids(client, detector_id, num, finding_type, severity):
    finding_criteria = {
        "Criterion": {
            "severity": {"Gte": severity_defaults[severity]},
        }
    }
    if finding_type:
        finding_criteria["Criterion"]["type"] = {"Eq": [finding_type]}
    
    return client.list_findings(
        DetectorId=detector_id,
        FindingCriteria=finding_criteria,
        SortCriteria={"AttributeName": "createdAt", "OrderBy": "DESC"},
        MaxResults=num,
    ).get("FindingIds", [])


def list_action(session, aws_region, profile, finding_id, num, finding_type, severity):
    account_id = session.client("sts").get_caller_identity()["Account"]
    if account_id in accounts_processed:
        return
    accounts_processed.append(account_id)

    regions = session.get_available_regions("guardduty") if aws_region == "all" else [aws_region]
    for region in regions:
        logging.debug(f"Checking {account_id} {profile} {region}")
        try:
            client = session.client("guardduty", region_name=region)
            
            detector_ids = list_detectors(client)
            if not detector_ids:
                logging.info(f"No detector is found. Skipped {account_id} {region}.")
                continue
            
            for detector_id in detector_ids:
                finding_ids = [finding_id] if finding_id else get_finding_ids(client, detector_id, num, finding_type, severity)
                findings = client.get_findings(DetectorId=detector_id, FindingIds=finding_ids).get("Findings", [])
                for finding in findings:
                    print("--------------------------------------------------------------------------------")
                    print(yaml.dump(finding))
                
                if finding_id and findings:
                    return findings[0]
                
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code in ["AuthFailure", "UnrecognizedClientException"]:
                logging.warning(f"Unable to process region {region}: {error_code}")
            elif error_code == "AccessDenied":
                logging.warning(f"Unable to process account {account_id}: {e}")
            elif error_code == "InvalidInstanceID.NotFound":
                pass
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
@click.option("--findingid", "-i", help="Finding ID. Optional.", default=None)
@click.option("--num", "-n", help="Number of records returned for each detector/account/region. Default: 5.", default=5)
@click.option("--findingtype", "-t", help="Recon Finding Type (e.g. Recon:IAMUser/UserPermissions). Optional.", default=None)
@click.option("--severity", "-s", help="Severity: high, medium, low. Default: high.", default="high")
@click.option("--region", "-r", help="AWS Region; use 'all' for all regions. Default: ap-southeast-2.", default="ap-southeast-2")
#@click.option("--detailed", "-d", is_flag=True)
def main(profile, region, findingid, num, findingtype, severity):
    profile_names = [profile] if profile else aws_profiles
    
    for profile_name in profile_names:
        try:
            session = Session(profile_name=profile_name)
            ret = list_action(session, region, profile_name, findingid, num, findingtype, severity)
            if ret is not None:
                break

        except ClientError as e:
            if e.response["Error"]["Code"] == "ExpiredToken":
                logging.warning(f"{profile_name} token expired. Skipped")
            else:
                raise


if __name__ == "__main__": main()

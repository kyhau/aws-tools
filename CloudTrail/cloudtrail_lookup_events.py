from boto3.session import Session
from botocore.exceptions import ClientError
import click
from configparser import ConfigParser
from datetime import datetime, timedelta
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


def process_account(session, event_name, user_name, start_time, end_time, max_results, aws_region, profile):
    account_id = session.client("sts").get_caller_identity()["Account"]
    if account_id in accounts_processed:
        return
    accounts_processed.append(account_id)

    end_dt = datetime.now() if end_time is None else datetime.strptime(end_time, "%Y-%m-%d")
    start_dt = end_dt - timedelta(hours=24) if start_time is None else datetime.strptime(start_time, "%Y-%m-%d")

    lookup_attributes = []  # If more than one attribute, they are evaluated as "OR".
    if event_name is not None:
        lookup_attributes.append({"AttributeKey": "EventName", "AttributeValue": event_name})
    if user_name is not None:
        lookup_attributes.append({"AttributeKey": "Username", "AttributeValue": user_name})

    operation_params = {"StartTime": start_dt, "EndTime": end_dt}
    if lookup_attributes:
        operation_params["LookupAttributes"] = lookup_attributes

    regions = session.get_available_regions("cloudtrail") if aws_region == "all" else [aws_region]
    for region in regions:
        logging.debug(f"Checking {account_id} {profile} {region}")
        try:
            client = session.client("cloudtrail", region_name=region)
            paginator = client.get_paginator("lookup_events")
            cnt = 0
            for page in paginator.paginate(**operation_params):
                for event in page["Events"]:
                    print("--------------------------------------------------------------------------------")
                    print(yaml.dump(event))
                    cnt += 1
                    if max_results is not None and cnt >= int(max_results):
                        break
                if max_results is not None and cnt >= int(max_results):  # enough results for this region
                    break
        
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
@click.option("--eventname", "-n", help="Event name. If specify both eventname and username, the condition is OR.", default=None)
@click.option("--username", "-u", help="User name. If specify both eventname and username, the condition is OR.", default=None)
@click.option("--starttime", "-s", help="Start time (e.g. 2020-04-01); return last 1d records if not specified", default=None)
@click.option("--endtime", "-e", help="End time (e.g. 2020-04-01); now if not specified.", default=None)
@click.option("--maxresults", "-m", help="Number of events to return for each account/region; unlimited if not specified.", default=None)
@click.option("--region", "-r", help="AWS Region; use 'all' for all regions.", default="ap-southeast-2")
def main(profile, eventname, username, starttime, endtime, maxresults, region):
    profile_names = [profile] if profile else aws_profiles
    
    for profile_name in profile_names:
        try:
            session = Session(profile_name=profile_name)
            process_account(session, eventname, username, starttime, endtime, maxresults, region, profile_name)
        
        except ClientError as e:
            if e.response["Error"]["Code"] in ["ExpiredToken", "InvalidClientTokenId", "AccessDeniedException"]:
                logging.warning(f'{profile_name} {e.response["Error"]["Code"]}. Skipped')
            else:
                raise


if __name__ == "__main__": main()

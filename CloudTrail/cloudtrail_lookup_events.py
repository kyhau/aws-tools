"""
A helper script for retrieving CloudTrail events
"""
import json
import logging

import click
from botocore.exceptions import ProfileNotFound
from helper.aws import AwsApiHelper
from helper.date_time import DT_FORMAT_YMDHMS, lookup_range_str_to_timestamp
from helper.ser import dump_json

logging.getLogger().setLevel(logging.DEBUG)

LOOKUP_HOURS = 4


class Helper(AwsApiHelper):
    def __init__(self, decode_json, max_results):
        super().__init__()
        self._decode_json = decode_json
        self._max_results = max_results

    def process_request(self, session, account_id, region, kwargs):
        client = session.client("cloudtrail", region_name=region)
        cnt = 0
        for event in self.paginate(client, "lookup_events", kwargs):
            print("--------------------------------------------------------------------------------")
            if self._decode_json:
                event["CloudTrailEvent"] = json.loads(event.get("CloudTrailEvent", ""))
            print(dump_json(event))
            cnt += 1
            if self._max_results is not None and cnt >= int(self._max_results):
                return


def new_operation_params(start_time, end_time, event_name, user_name):
    start_dt, end_dt = lookup_range_str_to_timestamp(start_time, end_time, lookup_hours=LOOKUP_HOURS, local_to_utc=True)

    lookup_attributes = []  # If more than one attribute, they are evaluated as "OR".
    if event_name is not None:
        lookup_attributes.append({"AttributeKey": "EventName", "AttributeValue": event_name})
    if user_name is not None:
        lookup_attributes.append({"AttributeKey": "Username", "AttributeValue": user_name})

    operation_params = {"StartTime": start_dt, "EndTime": end_dt}
    if lookup_attributes:
        operation_params["LookupAttributes"] = lookup_attributes

    return operation_params


@click.command()
@click.option("--eventname", "-n", help="Event name. If specify both eventname and username, the condition is OR.")
@click.option("--username", "-u", help="User name. If specify both eventname and username, the condition is OR.")
@click.option("--starttime", "-s", help=f"Start time ({DT_FORMAT_YMDHMS}); return records of last {LOOKUP_HOURS} hours if not specified.")
@click.option("--endtime", "-e", help=f"End time ({DT_FORMAT_YMDHMS}); now if not specified.")
@click.option("--maxresults", "-m", help="Number of events to return for each account/region; unlimited if not specified.")
@click.option('--decode', '-d', show_default=True, is_flag=True, help="Deserialize json-string to json-object")
@click.option("--profile", "-p", help="AWS profile name. Use profiles in ~/.aws if not specified.")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS Region. Use 'all' for all regions.")
def main(eventname, username, starttime, endtime, maxresults, decode, profile, region):
    kwargs = new_operation_params(starttime, endtime, eventname, username)

    try:
        Helper(decode, maxresults).start(profile, region, "cloudtrail", kwargs)
    except ProfileNotFound as e:
        logging.error(f"{e}. Aborted")


if __name__ == "__main__":
    main()

from botocore.exceptions import ProfileNotFound
import click
from datetime import datetime, timedelta
import logging
from arki_common.aws import AwsApiHelper
from arki_common.ser import dump_json

logging.getLogger().setLevel(logging.DEBUG)


class Helper(AwsApiHelper):
    def __init__(self, max_results):
        super().__init__()
        self._max_results = max_results

    def process_request(self, session, account_id, region, kwargs):
        client = session.client("cloudtrail", region_name=region)
        cnt = 0
        for event in self.paginate(client, "lookup_events", kwargs):
            print("--------------------------------------------------------------------------------")
            print(dump_json(event))
            cnt += 1
            if self._max_results is not None and cnt >= int(self._max_results):
                return


def new_operation_params(start_time, end_time, event_name, user_name):
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
    return operation_params


@click.command()
@click.option("--eventname", "-n", help="Event name. If specify both eventname and username, the condition is OR.")
@click.option("--username", "-u", help="User name. If specify both eventname and username, the condition is OR.")
@click.option("--starttime", "-s", help="Start time (e.g. 2020-04-01); return last 1d records if not specified.")
@click.option("--endtime", "-e", help="End time (e.g. 2020-04-01); now if not specified.")
@click.option("--maxresults", "-m", help="Number of events to return for each account/region; unlimited if not specified.")
@click.option("--profile", "-p", help="AWS profile name. Use profiles in ~/.aws if not specified.")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS Region. Use 'all' for all regions.")
def main(eventname, username, starttime, endtime, maxresults, profile, region):
    kwargs = new_operation_params(starttime, endtime, eventname, username)

    try:
        Helper(maxresults).start(profile, region, "cloudtrail", kwargs)
    except ProfileNotFound as e:
        logging.error(f"{e}. Aborted")


if __name__ == "__main__":
    main()

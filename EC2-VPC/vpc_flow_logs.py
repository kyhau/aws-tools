"""
Retrieve VPC Flow Logs with CloudWatch Logs Insights
"""
from time import sleep

import click
from boto3.session import Session
from helper.datetime import DT_FORMAT_YMDHMS, lookup_range_str_to_timestamp

LOOKUP_HOURS = 1

DEFAULT_QUERY_STRING = "fields @timestamp, @message | sort @timestamp asc"


@click.command(help="Retrieve VPC Flow Logs")
@click.option("--loggroupname", "-l", help="Log Group name", required=True)
@click.option("--starttime", "-s", help=f"Start time ({DT_FORMAT_YMDHMS}); return records of last {LOOKUP_HOURS} hours if not specified.")
@click.option("--endtime", "-e", help="End time ({DT_FORMAT_YMDHMS}); now if not specified.")
@click.option("--limit", "-m", type=int, default=10000, show_default=True, help="The maximum number of log events to return in the query.")
@click.option("--profile", "-p", default="default", show_default=True, help="AWS profile name.")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS Region.")
def main(loggroupname, starttime, endtime, limit, profile, region):
    session = Session(profile_name=profile)
    client = session.client("logs", region_name=region)

    start_dt, end_dt = lookup_range_str_to_timestamp(starttime, endtime, lookup_hours=LOOKUP_HOURS, local_to_utc=False)

    query_id = client.start_query(
        logGroupName=loggroupname,
        startTime=int(start_dt.timestamp()),  # Although doc says this is the number of seconds UTC, it takes local time and convert to UTC
        endTime=int(end_dt.timestamp()),
        queryString=DEFAULT_QUERY_STRING,
        limit=limit,
    )["queryId"]

    # TODO What if more than 10000 messages?

    response = None   # "Scheduled"|"Running"|"Complete"|"Failed"|"Cancelled"
    while response is None or response.get("status") == "Running":
        response = client.get_query_results(queryId=query_id)
        sleep(1)

    cnt = 0
    for item in response.get("results", []):
        v = [k["value"] for k in item if k["field"] == "@message"][0]
        t = [k["value"] for k in item if k["field"] == "@timestamp"][0]
        print(t, v)
        cnt += 1

    print(f"Number of items returned: {cnt}")


if __name__ == "__main__":
    main()

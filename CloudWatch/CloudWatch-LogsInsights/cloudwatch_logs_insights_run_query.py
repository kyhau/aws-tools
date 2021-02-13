"""
Run and retrieve results of CloudWatch Log Insight query
"""
import json
from time import sleep

import click
import yaml
from boto3.session import Session
from helper.datetime import DT_FORMAT_YMDHMS, lookup_range_str_to_timestamp

LOOKUP_HOURS = 4

DEFAULT_QUERY_STRING = """
fields @timestamp, @message
| sort @timestamp desc
""".replace("\n", " ").strip()


def read_file(filename):
    with open(filename, "r") as query_file:
        content = query_file.read()
    return content.replace("\n", " ").strip()


@click.command(help="Run and retrieve results of CloudWatch Log Insight query")
@click.option("--loggroupname", "-l", help="Log Group name", required=True)
@click.option("--starttime", "-s", help=f"Start time ({DT_FORMAT_YMDHMS}); return records of last {LOOKUP_HOURS} hours if not specified.")
@click.option("--endtime", "-e", help="End time ({DT_FORMAT_YMDHMS}); now if not specified.")
@click.option("--queryfile", "-f", help="Query file.")
@click.option("--limit", "-m", type=int, default=1, show_default=True, help="The maximum number of log events to return in the query.")
@click.option("--profile", "-p", default="default", show_default=True, help="AWS profile name.")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS Region.")
def main(loggroupname, starttime, endtime, queryfile, limit, profile, region):
    session = Session(profile_name=profile)
    client = session.client("logs", region_name=region)

    start_dt, end_dt = lookup_range_str_to_timestamp(starttime, endtime, lookup_hours=LOOKUP_HOURS, local_to_utc=False)

    query_string = read_file(queryfile) if queryfile else DEFAULT_QUERY_STRING

    query_id = client.start_query(
        logGroupName=loggroupname,
        startTime=int(start_dt.timestamp()),  # Although doc says this is the number of seconds UTC, it takes local time and convert to UTC
        endTime=int(end_dt.timestamp()),
        queryString=query_string,
        limit=limit,  # This value overrides the limit specified in the queryString
    )["queryId"]

    response = None
    # Valid status: 'Scheduled'|'Running'|'Complete'|'Failed'|'Cancelled'
    while response is None or response.get("status") in ["Running", "Scheduled"]:
        response = client.get_query_results(queryId=query_id)
        sleep(1)

    cnt = 0
    for item in response.get("results", []):
        cnt += 1
        print(f"# Item {cnt} --------------------")
        print(yaml.dump({
            field["field"]: json.loads(field["value"]) if field["value"][0] == "{" else field["value"]
            for field in item if field["field"] != "@ptr"
        }))
    print(f"Number of items returned: {cnt}")

if __name__ == "__main__":
    main()

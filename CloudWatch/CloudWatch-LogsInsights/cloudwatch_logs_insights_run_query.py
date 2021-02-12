import json
import logging
from datetime import datetime, timedelta

import click
import yaml
from boto3.session import Session

logging.getLogger().setLevel(logging.DEBUG)

LOOKUP_HOURS = 12

default_query_string = """
fields @timestamp, @message
| sort @timestamp desc
| limit 20
""".replace("\n", " ").strip()


def read_file(filename):
    with open(filename, "r") as query_file:
        content = query_file.read()
    return content.replace("\n", " ").strip()


@click.command()
@click.option("--profile", "-p", help="AWS profile name.", default="default")
@click.option("--loggroupname", "-l", help="Log Group name", required=True)
@click.option("--starttime", "-s", help=f"Start time (e.g. 2020-04-01); return last {LOOKUP_HOURS} records if not specified", default=None)
@click.option("--endtime", "-e", help="End time (e.g. 2020-04-01); now if not specified.", default=None)
@click.option("--queryfile", "-f", help="Query file.", default=None)
@click.option("--region", "-r", help="AWS Region. Default ap-southeast-2", default="ap-southeast-2")
def main(profile, loggroupname, starttime, endtime, queryfile, region):
    session = Session(profile_name=profile)
    client = session.client("logs", region_name=region)

    end_dt = datetime.now() if endtime is None else datetime.strptime(endtime, "%Y-%m-%d")
    start_dt = end_dt - timedelta(hours=LOOKUP_HOURS) if starttime is None else datetime.strptime(starttime, "%Y-%m-%d")

     # Convert local datetime to UTC
    local_to_utc = lambda dt: datetime.utcfromtimestamp(datetime.timestamp(dt))

    end_dt = local_to_utc(end_dt)
    start_dt = local_to_utc(start_dt)

    query_string = read_file(queryfile) if queryfile else default_query_string

    query_id = client.start_query(
        logGroupName=loggroupname,
        startTime=int(start_dt),
        endTime=int(end_dt),
        queryString=query_string,
    )["queryId"]

    status = "Running"    # 'Scheduled'|'Running'|'Complete'|'Failed'|'Cancelled'
    while status == "Running":
        response = client.get_query_results(queryId=query_id)
        for item in response.get("results", []):
            print("----------")
            print(yaml.dump({
                field["field"]: json.loads(field["value"]) if field["value"][0] == "{" else field["value"]
                for field in item if field["field"] != "@ptr"
            }))
        status = response.get("status")


if __name__ == "__main__":
    main()

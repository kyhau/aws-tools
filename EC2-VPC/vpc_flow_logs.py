"""
Retrieve VPC Flow Logs with CloudWatch Logs Insights
"""
import logging
from datetime import datetime, timedelta

import click
from boto3.session import Session

logging.getLogger().setLevel(logging.DEBUG)

LOOKUP_HOURS = 1


@click.command(help="Retrieve VPC Flow Logs")
@click.option("--profile", "-p", help="AWS profile name.", default="default")
@click.option("--loggroupname", "-l", help="Log Group name", required=True)
@click.option("--starttime", "-s", help="Start time (e.g. 2020-04-01 04:00:00); return last 1d records if not specified")
@click.option("--endtime", "-e", help="End time (e.g. 2020-04-01 04:30:00); now if not specified.")
@click.option("--region", "-r", help="AWS Region. Default ap-southeast-2", default="ap-southeast-2")
def main(profile, loggroupname, starttime, endtime, region):
    session = Session(profile_name=profile)
    client = session.client("logs", region_name=region)

    end_dt = datetime.now() if endtime is None else datetime.strptime(endtime, "%Y-%m-%d %H:%M:%S")
    start_dt = (end_dt - timedelta(hours=LOOKUP_HOURS)) if starttime is None else datetime.strptime(starttime, "%Y-%m-%d %H:%M:%S")

    # Convert local datetime to UTC
    #local_to_utc = lambda dt: datetime.utcfromtimestamp(datetime.timestamp(dt))
    #start_dt = local_to_utc(start_dt)
    #end_dt = local_to_utc(end_dt)

    start_timestamp = int(start_dt.timestamp())
    end_timestamp = int(end_dt.timestamp())

    query_string = 'fields @timestamp, @message | sort @timestamp asc'

    check_timestamp = start_timestamp

    while check_timestamp < end_timestamp:
        print(check_timestamp)

        query_id = client.start_query(
            logGroupName=loggroupname,
            startTime=check_timestamp,
            endTime=check_timestamp+1,
            queryString=query_string,
            limit=10000,
        )["queryId"]

        response = None   # 'Scheduled'|'Running'|'Complete'|'Failed'|'Cancelled'
        while response is None or response.get("status") == "Running":
            response = client.get_query_results(queryId=query_id)

        # TODO What if more than 10000 messages?

        for item in response.get("results", []):
            v = [k['value'] for k in item if k['field'] == '@message'][0]
            t = [k['value'] for k in item if k['field'] == '@timestamp'][0]
            print(t, v)

        check_timestamp += 1



if __name__ == "__main__":
    main()

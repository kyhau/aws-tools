"""
Retrieve VPC Flow Logs with CloudWatch Logs Insights
"""
from boto3.session import Session
import click
from datetime import datetime, timedelta
import logging

logging.getLogger().setLevel(logging.DEBUG)


LOOKUP_HOURS = 12


@click.command(help="Retrieve VPC Flow Logs")
@click.option("--profile", "-p", help="AWS profile name.", default="default")
@click.option("--loggroupname", "-l", help="Log Group name", required=True)
@click.option("--starttime", "-s", help="Start time (e.g. 2020-04-01); return last 1d records if not specified", default=None)
@click.option("--endtime", "-e", help="End time (e.g. 2020-04-01); now if not specified.", default=None)
@click.option("--region", "-r", help="AWS Region. Default ap-southeast-2", default="ap-southeast-2")
def main(profile, loggroupname, starttime, endtime, region):
    session = Session(profile_name=profile)
    client = session.client("logs", region_name=region)

    end_dt = datetime.now() if endtime is None else datetime.strptime(endtime, "%Y-%m-%d")
    start_dt = end_dt - timedelta(hours=LOOKUP_HOURS) if starttime is None else datetime.strptime(starttime, "%Y-%m-%d")
    query_string = "fields @timestamp, @message | sort @timestamp desc"
    
    query_id = client.start_query(
        logGroupName=loggroupname,
        startTime=int(start_dt.timestamp()),
        endTime=int(end_dt.timestamp()),
        queryString=query_string,
    )["queryId"]

    status = "Running"    # 'Scheduled'|'Running'|'Complete'|'Failed'|'Cancelled'
    while status == "Running":
        response = client.get_query_results(queryId=query_id)
        for item in response.get("results", []):
            v = [k['value'] for k in item if k['field'] == '@message'][0]
            t = [k['value'] for k in item if k['field'] == '@timestamp'][0]
            print(t, v)

        status = response.get("status")


if __name__ == "__main__":
    main()

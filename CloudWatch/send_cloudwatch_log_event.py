"""
Create and send sample CloudWatch log group event
"""
import time

import click
from boto3.session import Session

LOGSTREAM=f"{time.strftime('%Y-%m-%d-%H-%M-%S')}-logstream"


def send_sample_cloudwatch_loggroup_event(client, loggroup, logstream):
    """
    try:
        client.create_loggroup(logGroupName=loggroup)
    except client.exceptions.ResourceAlreadyExistsException:
        pass
    """

    try:
        client.create_log_stream(logGroupName=loggroup, logStreamName=logstream)
    except client.exceptions.ResourceAlreadyExistsException:
        pass

    resp = client.describe_log_streams(logGroupName=loggroup, logStreamNamePrefix=logstream)

    event_log = {
        "logGroupName": loggroup,
        "logStreamName": logstream,
        "logEvents": [
            {
                "timestamp": int(round(time.time() * 1000)),
                "message": time.strftime("%Y-%m-%d %H:%M:%S") + "  Your custom log messages"
            }
        ],
    }

    if "uploadSequenceToken" in resp["logStreams"][0]:
        event_log.update({"sequenceToken": resp["logStreams"][0]["uploadSequenceToken"]})

    resp = client.put_log_events(**event_log)
    print(resp)
    assert(resp["HTTPStatusCode"] == 200)


@click.command(help="Create and send sample CloudWatch log group event")
@click.argument("loggroup", help="CloudWatch log group name")
@click.option("--logstream", "-s", default=LOGSTREAM, help="Log stream name; will be created if not exists")
@click.option("--profile", "-p", default="default", show_default=True, help="AWS profile name")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS Region")
def main(loggroup, logstream, profile, region):
    client = Session(profile_name=profile).client("logs", region=region)
    send_sample_cloudwatch_loggroup_event(client, loggroup, logstream)


if __name__ == "__main__":
     main()

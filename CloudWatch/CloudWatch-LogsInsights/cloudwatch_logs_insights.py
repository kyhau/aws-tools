'''
Run and retrieve results of CloudWatch Log Insight query
'''
import json
from time import sleep

import click
import yaml
from boto3.session import Session
from helper.date_time import DT_FORMAT_YMDHMS, lookup_range_str_to_timestamp

LOOKUP_HOURS = 4

PREDEFINED_QUERIES = {
    'Default': 'fields @timestamp, @message | sort @timestamp desc',
    'CreateUser': 'fields awsRegion, requestParameters.userName, responseElements.user.arn | filter eventName="CreateUser"',
    'S3PresignedUrl': 'fields @timestamp, @message | filter eventSource = "s3.amazonaws.com" and (eventName = "GetObject" or eventName = "PutObject") and ispresent(requestParameters.Expires) | sort @timestamp desc',
}

@click.group(invoke_without_command=False, help='Run and retrieve results of CloudWatch Log Insights query')
def main_cli():
    pass


@main_cli.command(help='Run and retrieve results of CloudWatch Log Insights query')
@click.option('--ls', '-l', is_flag=True, show_default=True, help='List predefined query strings')
@click.option('--loggroupname', '-n', help='Log Group name', required=True)
@click.option('--starttime', '-s', help=f'Start time ({DT_FORMAT_YMDHMS}); return records of last {LOOKUP_HOURS} hours if not specified.')
@click.option('--endtime', '-e', help=f'End time ({DT_FORMAT_YMDHMS}); now if not specified.')
@click.option('--querystring', '-t', help='Query string (e.g. fields @timestamp, @message | sort @timestamp desc)')
@click.option('--limit', '-m', type=int, default=1, show_default=True, help='The maximum number of log events to return in the query.')
@click.option('--profile', '-p', default='default', show_default=True, help='AWS profile name.')
@click.option('--region', '-r', default='ap-southeast-2', show_default=True, help='AWS Region.')
def query(ls, loggroupname, starttime, endtime, querystring, limit, profile, region):
    session = Session(profile_name=profile)
    client = session.client('logs', region_name=region)

    start_dt, end_dt = lookup_range_str_to_timestamp(starttime, endtime, lookup_hours=LOOKUP_HOURS, local_to_utc=False)

    query_string = querystring if querystring else PREDEFINED_QUERIES['Default']

    query_id = client.start_query(
        logGroupName=loggroupname,
        startTime=int(start_dt.timestamp()),  # Although doc says this is the number of seconds UTC, it takes local time and convert to UTC
        endTime=int(end_dt.timestamp()),
        queryString=query_string,
        limit=limit,  # This value overrides the limit specified in the queryString
    )['queryId']

    response = None
    # Valid status: 'Scheduled'|'Running'|'Complete'|'Failed'|'Cancelled'
    while response is None or response.get('status') in ['Running', 'Scheduled']:
        response = client.get_query_results(queryId=query_id)
        sleep(1)

    cnt = 0
    for item in response.get('results', []):
        cnt += 1
        print(f'# Item {cnt} --------------------')
        print(yaml.dump({
            field['field']: json.loads(field['value']) if field['value'][0] == '{' else field['value']
            for field in item if field['field'] != '@ptr'
        }))
    print(f'Number of items returned: {cnt}')


@main_cli.command(help='List log groups')
@click.option('--loggroupnameprefix', '-n', help='Log Group Name Prefix', required=False)
@click.option('--profile', '-p', default='default', show_default=True, help='AWS profile name.')
@click.option('--region', '-r', default='ap-southeast-2', show_default=True, help='AWS Region.')
def loggroups(loggroupnameprefix, profile, region):
    session = Session(profile_name=profile)
    client = session.client('logs', region_name=region)

    params = {"logGroupNamePrefix": loggroupnameprefix} if loggroupnameprefix else {}
    for page in client.get_paginator("describe_log_groups").paginate(**params).result_key_iters():
        for item in page:
            print(item["logGroupName"])



@main_cli.command(help='List predefined query strings')
def ls():
    for k, v in PREDEFINED_QUERIES.items():
        print(f'{k}: {v}')


if __name__ == '__main__':
    main_cli()

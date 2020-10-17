import json
import logging
import os

import boto3

logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('urllib3.connectionpool').setLevel(logging.CRITICAL)
logging.info(f'boto3.__version__: {boto3.__version__}')

client = boto3.client('logs')

LOGGROUP_PREFIX = os.environ.get('LOGGROUP_PREFIX')
RETENTION_DAYS = os.environ.get('RETENTION_DAYS', 1)

def lambda_handler(event, context):
    params = {} if LOGGROUP_PREFIX is None else {'logGroupNamePrefix': LOGGROUP_PREFIX}

    for page in client.get_paginator('describe_log_groups').paginate(**params).result_key_iters():
        for item in page:
            loggroup_name = item['logGroupName']
            retention = item['retentionInDays']
            logging.info(f'{loggroup_name}, {retention}')

            if RETENTION_DAYS != retention:
                logging.info(f'Updating {loggroup_name} to {RETENTION_DAYS}')

                resp = client.put_retention_policy(
                    logGroupName=loggroup_name,
                    retentionInDays=RETENTION_DAYS,
                )
                logging.info(resp)

    body = {
        'message': 'succeed',
    }

    response = {
        'statusCode': 200,
        'body': json.dumps(body)
    }

    return response


lambda_handler(None, None)

import json
import logging
import os
import time

import boto3

SFN_ARN = os.environ["sfnArn"]
EXE_ARN = SFN_ARN.replace(":stateMachine:", ":execution:")

sfn_client = boto3.client("stepfunctions")


def lambda_response(message, status_code=200):
    logging.info(message)
    return {
        "body": json.dumps(message),
        "headers": {"Content-Type": "application/json"},
        "statusCode": status_code,
    }


def lambda_handler(event, context):
    logging.info(event)
    logging.info(SFN_ARN)

    params = event["queryStringParameters"]
    eid = params.get("eid")

    if eid:
        resp = sfn_client.describe_execution(executionArn=f"{EXE_ARN}:{eid}")
        while resp["status"] == "RUNNING":
            print(resp.get("output"))
            time.sleep(1)
            resp = sfn_client.describe_execution(executionArn=f"{EXE_ARN}:{eid}")

        print(resp.get("output"))
        return lambda_response(resp.get("output"))

    return lambda_response({"message": f"Returned from lambda B {eid}"})

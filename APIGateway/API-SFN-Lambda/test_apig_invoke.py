"""
aws apigateway test-invoke-method --rest-api-id todo_apig_id --resource-id todo_resource_id --http-method POST
"""
import json

import boto3

API_ID = "todo_apig_id"
START_RESOURCE_ID = "todo_resource_id"
SFN_ARN = "arn:aws:states:ap-southeast-2:1231456789012:stateMachine:K-SFN-StateMachine"
EXE_ARN = lambda arn: arn.replace(":stateMachine:", ":execution:")

apig_client = boto3.client("apigateway")


def test_apig_invoke(sfn_arn):

    # Start an execution
    resp = apig_client.test_invoke_method(
        restApiId=API_ID,
        resourceId=START_RESOURCE_ID,
        httpMethod="POST",
        stageVariables={"sfnArn": sfn_arn}
    )
    body = json.loads(resp["body"])
    sfn_exec_token = body.get("token")
    print(resp if sfn_exec_token is None else f"Token: {sfn_exec_token}")
    assert(sfn_exec_token)

    # Retrieve result from the execution
    print("Retrieve result from the execution:")
    resp = apig_client.test_invoke_method(
        restApiId=API_ID,
        resourceId=START_RESOURCE_ID,
        httpMethod="GET",
        pathWithQueryString= f"/?eid={sfn_exec_token}"
    )
    body = json.loads(resp["body"])
    print(body)


test_apig_invoke(SFN_ARN)

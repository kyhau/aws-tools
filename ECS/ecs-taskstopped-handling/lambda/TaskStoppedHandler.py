"""
This is a Lambda function to be triggered from CloudWatch Events (ECS Task Stopped).
"""
import boto3
import json
import logging


# Update the root logger to get messages at DEBUG and above
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger("botocore").setLevel(logging.CRITICAL)
logging.getLogger("boto3").setLevel(logging.CRITICAL)
logging.getLogger("urllib3.connectionpool").setLevel(logging.CRITICAL)

logging.info(f"boto3.__version__: {boto3.__version__}")


def lambda_handler(event, context):
    """
    Main entry point when triggering the AWS Lambda function.

    :param event: a dictionary of event information from AWS ECS Task Stopped event
    :param context: a dictionary of runtime information from AWS ECS

    Example of `event`: (taskArn is the task_id in DynamoDB)
        "version": "0",
        "id": "xxxx",
        "detail-type": "ECS Task State Change",
        "source": "aws.ecs",
        "account": "111122223333",
        "time": "2019-06-30T03:36:57Z",
        "region": "ap-southeast-2",
        "resources": [
            "arn:aws:ecs:ap-southeast-2:111122223333:task/xxxx"
        ],
        "detail": {
            "clusterArn": "arn:aws:ecs:ap-southeast-2:111122223333:cluster/Orca-Cluster",
            "containerInstanceArn": "arn:aws:ecs:ap-southeast-2:111122223333:container-instance/xxxx",
            "containers": [
                {
                    "containerArn": "arn:aws:ecs:ap-southeast-2:111122223333:container/xxxx",
                    "exitCode": 1,
                    "lastStatus": "STOPPED",
                    "name": "sample_app-1_0_0",
                    "taskArn": "arn:aws:ecs:ap-southeast-2:111122223333:task/xxxx",
                    "networkInterfaces": [],
                    "cpu": "4",
                    "memory": "1024"
                }
            ],
            "createdAt": "2019-06-30T03:36:53.763Z",
            "launchType": "EC2",
            "cpu": "4",
            "memory": "1024",
            "desiredStatus": "STOPPED",
            "group": "family:sample_app-1_0_0",
            "lastStatus": "STOPPED",
            "overrides": {
                "containerOverrides": [
                    {
                        "environment": [
                            {
                                "name": "S3_BUCKET",
                                "value": "bucket-name-xxx"
                            }
                        ],
                        "name": "sample_app-1_0_0"
                    }
                ]
            },
            "attachments": [],
            "connectivity": "CONNECTED",
            "connectivityAt": "2019-06-30T03:36:53.763Z",
            "pullStartedAt": "2019-06-30T03:36:55.311Z",
            "startedAt": "2019-06-30T03:36:56.311Z",
            "stoppingAt": "2019-06-30T03:36:57.935Z",
            "stoppedAt": "2019-06-30T03:36:57.935Z",
            "pullStoppedAt": "2019-06-30T03:36:55.311Z",
            "executionStoppedAt": "2019-06-30T03:36:57Z",
            "stoppedReason": "Essential container in task exited",
            "stopCode": "EssentialContainerExited",
            "updatedAt": "2019-06-30T03:36:57.935Z",
            "taskArn": "arn:aws:ecs:ap-southeast-2:111122223333:task/xxxx",
            "taskDefinitionArn": "arn:aws:ecs:ap-southeast-2:111122223333:task-definition/sample_app-1_0_0:1",
            "version": 3
        }
    }
    """
    logging.debug("Received event: " + json.dumps(event))

    if event["source"] != "aws.ecs":
        raise ValueError("Function only supports input from events with a source type of: aws.ecs")

    # Extract data from event
    params = {
        "timestamp": event["detail"]["stoppedAt"],
        "task_arn": event["detail"]["taskArn"],
        "other_env_data": event["detail"]["overrides"]["containerOverrides"][0]["environment"],
    }
    return process_ecs_task_stopped_event(params)


def process_ecs_task_stopped_event(params):
    # TODO
    return 0

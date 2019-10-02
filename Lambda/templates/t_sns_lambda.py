"""
This is a Lambda function to be triggered from SNS and update a DynamoDB table accordingly.
"""
import boto3
from botocore.exceptions import ClientError
import json
import logging

# Update the root logger to get messages at DEBUG and above
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger("botocore").setLevel(logging.CRITICAL)
logging.getLogger("boto3").setLevel(logging.CRITICAL)
logging.getLogger("urllib3.connectionpool").setLevel(logging.CRITICAL)

logging.info(f"boto3.__version__: {boto3.__version__}")


# To be used as the subject of SNS to identify event categories
DEFAULT_SUBJECTS = [
    "STARTED",
    "CANCELLED",
    "STOPPED",
]


def process_sns_record(record):
    """
    Process a record in the SNS message
    :param record: a record in the SNS message
    :return: response
    :raise UnrecognizedEventError if subject not matched any supported states.
    """
    subject = record["Subject"].upper()
    message = json.loads(record["Message"])

    if subject not in DEFAULT_SUBJECTS:
        raise UnrecognizedEventError(f"Unknown subject {subject}")

    if subject == "STARTED":
        pass
    elif subject == "CANCELLED":
        pass
    else:
        pass


def lambda_handler(event, context):
    """
    Main entry point when triggering the AWS Lambda function.

    :param event: a dictionary of event information from AWS Lambda
    :param context: a dictionary of runtime information from AWS Lambda

    Example of `event`:
    {
      "Records": [{
        "EventSource": "aws:sns",
        "EventVersion": "1.0",
        "EventSubscriptionArn": "arn:aws:sns:ap-southeast-2:111122223333:SNS-Example:xxxx",
        "Sns": {
            "Type": "Notification",
            "MessageId": "xxxx",
            "TopicArn": "arn:aws:sns:ap-southeast-2:111122223333:SNS-ExampleTopic",
            "Subject": "STARTED",
            "Message": "(string with context like {
              "task_id": "",
              "user_id": "xxx,
              "app_data": ...
            }",
            "Timestamp": "2018-02-18T07:11:21.131Z",
            "SignatureVersion": "1",
            "Signature": "xxx",
            "SigningCertUrl": "xxx",
            "UnsubscribeUrl": "xxx",
            "MessageAttributes": {}
        }
      }]
    }
    """
    logging.debug("Received event: " + json.dumps(event))

    # Note: Although `Records` is a list. But it comes with only one message at a time.
    # See https://aws.amazon.com/sns/faqs/#reliability
    #   Q: Will a notification contain more than one message?
    #   No, all notification messages will contain a single published message.

    response = process_sns_record(event["Records"][0]["Sns"])

    if len(event["Records"]) != 1:
        raise LambdaError(f"Lambda received SNS message contains more than one record: {json.dumps(event)}")

    return response


class LambdaError(Exception):
    # Default value; override in subclasses.
    response_code = 500

    def __init__(self, message):
        Exception.__init__(self, f"{self.response_code} {message}")


class UnrecognizedEventError(LambdaError):
    response_code = 400

"""
This is a Lambda function to be triggered from SNS and update a DynamoDB table accordingly.
"""
from decimal import Decimal
import json
import logging
from os import environ

import boto3
from botocore.exceptions import ClientError

# Update the root logger to get messages at DEBUG and above
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger("botocore").setLevel(logging.CRITICAL)
logging.getLogger("boto3").setLevel(logging.CRITICAL)
logging.getLogger("urllib3.connectionpool").setLevel(logging.CRITICAL)

logging.info(f"boto3.__version__: {boto3.__version__}")

# Default DynamoDB Table Name
DEFAULT_TABLE_NAME = "SimpleDDB"

# Key field in the DynamoDB Table
KEY_ID_FIELD = "key_id"

STATE_FIELD = "state"

# Time fields in the DynamoDB Table
# Expected format: e.g. 2018-02-12T02:11:21.348Z (the timestamp field attached to a AWS request/response
REQUEST_START_TIME_FIELD = "request_start_time"
REQUEST_STOP_TIME_FIELD = "request_stop_time"

# Mandatory fields required of a new item
MANDATORY_FIELDS = [KEY_ID_FIELD, STATE_FIELD]


def settings():
    """Settings to be passed to the Lambda functions environment variables"""
    return {"table_name": environ.get("DYNAMODB_TABLE_NAME", DEFAULT_TABLE_NAME)}


class DdbHelper:
    """Helper class for updating DynamoDB table."""
    def __init__(self, table_name):
        self.table = self._init_client_table(table_name)

    def _init_client_table(self, table_name):
        return boto3.resource("dynamodb").Table(table_name)

    def put_item(self, item):
        """
        Add new item to DynamoDB table

        :param item: dict object to be inserted
        :return: response
        :raise IDExistsError if item with the same key_id exists
        """
        try:
            return self.table.put_item(
                Item=item,
                ConditionExpression=f"attribute_not_exists({KEY_ID_FIELD})"
            )
        except ClientError as e:
            if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
                raise IDExistsError(f"{KEY_ID_FIELD} {item[KEY_ID_FIELD]} exists")
            raise

    def update_item(self, key_id, fields_to_update):
        """
        Update an existing item in the DynamoDB table

        :param key_id: the key_id of the existing item
        :param fields_to_update: dict of the field name and value to update
        :return: response
        :raise IDNotFoundError if no item with given key_id found
        """
        # Create UpdateExpression string e.g. field_name = :field_name,
        update_exp_str = ", ".join(f"{k} = :{k}" for k in fields_to_update.keys())

        # Create ExpressionAttributeValues e.g. {:field_name: field_value}
        exp_attr_values = {f":{k}": v for k, v in fields_to_update.items()}

        try:
            return self.table.update_item(
                Key={KEY_ID_FIELD: key_id},
                ConditionExpression=f"attribute_exists({KEY_ID_FIELD})",
                UpdateExpression=f"SET {update_exp_str}",
                ExpressionAttributeValues=exp_attr_values
            )
        except ClientError as e:
            if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
                raise IDNotFoundError(f"{KEY_ID_FIELD} {key_id} not found")
            raise

    def get_item(self, key_id):
        """
        Retrieve job of a given key_id from the DynamoDB table

        :param key_id: the key_id of the existing item
        :return: response
        :raise IDNotFoundError if no item with given key_id found
        """
        response = self.table.get_item(Key={KEY_ID_FIELD: key_id})
        if response.get("Item") is None:
            raise IDNotFoundError(f"{KEY_ID_FIELD} {key_id} not found")
        return response

    @staticmethod
    def validate_mandatory_fields(main_fields, input_data):
        """
        Check if all the given main_fields exist in the the input_data.

        :param main_fields: list of field names
        :param input_data: dict of {field_name, field_value}
        :return: dict of data matching main_fields
        :raise MissingDataError is any main_fields not found in input_data
        """
        missing_fields = [field for field in main_fields if field not in input_data]
        if missing_fields:
            message = f"Fields not provided: {missing_fields}"
            logging.error(message)
            raise MissingDataError(message)

        return {field: input_data[field] for field in main_fields}

    def fields_to_update(self, state, timestamp):
        """
        Determine the fields and values to be updated.

        :return: dict of fields to be updated
        :raises NoNewDataError: if the incoming SNS message had no new data to be updated in the DB
        """
        fields = {
            STATE_FIELD: state,
        }
        if state == "STARTED":
            fields[REQUEST_START_TIME_FIELD] = timestamp
        else:
            fields[REQUEST_STOP_TIME_FIELD] = timestamp
        return fields

    def process_sns_record(self, record):
        """
        Process a record in the SNS message, validate data and update the corresponding item in the DynamoDB table.

        :param record: a record in the SNS message
        :return: response
        :raise MissingDataError is any main_fields not found in input_data
        """
        subject = record["Subject"].upper()
        message = json.loads(record["Message"])

        if subject == "READY":
            item = self.validate_mandatory_fields(MANDATORY_FIELDS, message)
            item.update({STATE_FIELD: subject})
            item = _convert_data_for_dynamodb(item)
            response = self.put_item(item)
        else:
            key_id = self.validate_mandatory_fields([KEY_ID_FIELD], message)[KEY_ID_FIELD]
            fields = self.fields_to_update(
                state=subject,
                timestamp=record["Timestamp"],
            )
            fields = _convert_data_for_dynamodb(fields)
            response = self.update_item(key_id, fields)

            logging.debug(f"Response: {response}")
            if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
                raise LambdaError(
                    f"Lambda received response code: {response['ResponseMetadata']['HTTPStatusCode']}: {response}")
        return response


def _convert_data_for_dynamodb(data):
    """
    Perform minor data conversion for DynamoDB limitations.

    :param data: a dictionary of arbitrary data
    :return: a dictionary with data cleaned up
    """
    # Handle float to decimal conversion for DynamoDB
    data = json.loads(json.dumps(data), parse_float=Decimal)

    def _convert_empty_string_to_none(data):
        # nullify empty strings in `data`.
        if isinstance(data, str) and data == "":
            data = None
        elif isinstance(data, dict):
            for key, value in data.items():
                data[key] = _convert_empty_string_to_none(value)
        elif isinstance(data, list):
            for i in range(len(data)):
                data[i] = _convert_empty_string_to_none(data[i])
        return data

    # Convert empty string to None
    data = _convert_empty_string_to_none(data)
    return data


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

    handler = DdbHelper(settings()["table_name"])

    # Note: Although `Records` is a list. But it comes with only one message at a time.
    #
    # See https://aws.amazon.com/sns/faqs/#reliability
    #   Q: Will a notification contain more than one message?
    #   No, all notification messages will contain a single published message.

    response = handler.process_sns_record(event["Records"][0]["Sns"])

    if len(event["Records"]) != 1:
        raise LambdaError(f"Lambda received SNS message contains more than one record: {json.dumps(event)}")

    return response


class LambdaError(Exception):
    # Default value; override in subclasses.
    response_code = 500

    def __init__(self, message):
        Exception.__init__(self, f"{self.response_code} {message}")


class MissingDataError(LambdaError):
    response_code = 400


class IDExistsError(LambdaError):
    response_code = 400


class IDNotFoundError(LambdaError):
    response_code = 404

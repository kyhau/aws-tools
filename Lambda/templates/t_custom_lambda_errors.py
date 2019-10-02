"""
    try:
        return self.table.update_item(
            Key={"ID": id},
            ConditionExpression=f"attribute_exists(ID)",
            UpdateExpression=f"SET {update_exp_str}",
            ExpressionAttributeValues=exp_attr_values
        )
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            raise IDNotFoundError("ID not found")
        raise

    if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
        raise LambdaError(f"Lambda received response code: {response['ResponseMetadata']['HTTPStatusCode']}: {response}")

    raise LambdaError(f"Lambda received SNS message contains more than one record: {json.dumps(event)}")
"""


class LambdaError(Exception):
    # Default value; override in subclasses.
    response_code = 500

    def __init__(self, message):
        Exception.__init__(self, f"{self.response_code} {message}")


class UnrecognizedEventError(LambdaError):
    response_code = 400

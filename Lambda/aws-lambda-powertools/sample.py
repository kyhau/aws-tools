import os
import secrets

import boto3
from aws_lambda_powertools import Logger, Metrics, Tracer
from aws_lambda_powertools.metrics import MetricUnit
from botocore.exceptions import ClientError

logger = Logger()
tracer = Tracer()
metrics = Metrics()


session = boto3.Session()
dynamodb = session.resource("dynamodb")
table_name = os.getenv("BOOKING_TABLE_NAME", "undefined")
table = dynamodb.Table(table_name)


@tracer.capture_method
def confirm_booking(booking_id):
    try:
        reference = secrets.token_urlsafe(4)
        logger.debug(
            {
                "operation": "booking_confirmation",
                "details": {"booking_id": booking_id, "booking_reference": reference},
            }
        )
        ret = table.update_item(
            Key={"id": booking_id},
            ConditionExpression="id = :idVal",
            UpdateExpression="SET bookingReference = :br, #STATUS = :confirmed",
            ExpressionAttributeNames={"#STATUS": "status"},
            ExpressionAttributeValues={
                ":br": reference,
                ":idVal": booking_id,
                ":confirmed": "CONFIRMED",
            },
            ReturnValues="UPDATED_NEW",
        )

        logger.info({"operation": "booking_confirmation", "details": ret})
        tracer.put_metadata(booking_id, ret)

        return {"bookingReference": reference}
    except ClientError as err:
        logger.exception({"operation": "booking_confirmation"})
        raise


@metrics.log_metrics(capture_cold_start_metric=True)
def lambda_handler(event, context):
    booking_id = event.get("bookingId")
    if not booking_id:
        metrics.add_metric(name="InvalidConfirmationRequest", unit=MetricUnit.Count, value=1)
        logger.error({"operation": "input_validation", "details": event})
        raise ValueError("Invalid booking ID")

    try:
        logger.debug(f"Confirming booking - {booking_id}")
        ret = confirm_booking(booking_id)

        metrics.add_metric(name="SuccessfulBooking", unit=MetricUnit.Count, value=1)
        tracer.put_annotation("BookingReference", ret["bookingReference"])
        tracer.put_annotation("BookingStatus", "CONFIRMED")

        # Step Functions use the return to append `bookingReference` key into the overall output
        return ret["bookingReference"]
    except Exception as err:
        metrics.add_metric(name="FailedBooking", unit=MetricUnit.Count, value=1)
        tracer.put_annotation("BookingStatus", "ERROR")
        logger.exception({"operation": "booking_confirmation"})
        raise
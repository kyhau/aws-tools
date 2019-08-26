"""
Helper functions for retrieving events subscribed from SQS of CloudTrail
"""
import boto3
import gzip
import json
import os
import logging
from collections import defaultdict

QUEUE_URL = "https://ap-southeast-2.queue.amazonaws.com/todo_acc_id/xxx-Notifications"

#boto3.setup_default_session(profile_name=AWS_PROFILE)


def init_session(profile_name):
    """
    Return an aws session for the given aws profile
    """
    return boto3.session.Session(profile_name=profile_name)


def check_sqs_queue(profile):
    """
    Check the queue for completed files and set them to be downloaded.
    """
    session = init_session(profile["name"])
    sqs = session.resource("sqs", region_name=profile["cloudtrail.region"])

    # list all queues - test only
    #for queue in sqs.queues.all():
    #    logging.debug(queue.url)

    records = defaultdict(dict)

    queue = sqs.Queue(QUEUE_URL)
    for msg in queue.receive_messages(MaxNumberOfMessages=10, WaitTimeSeconds=20):

        body = json.loads(msg.body)
        message = body.get("Message", "{}")
        bucket = json.loads(message).get("s3Bucket", '')
        object_key = json.loads(message).get("s3ObjectKey")[0]
        filestore = profile["filestore"]

        parse_log(bucket, object_key, session, profile["cloudtrail.region"], filestore, records)
        msg.delete()

    return records


def parse_log(bucket_name, key, session, region_name, filestore, ret_records):
    """
    Return the events we care
    """

    local_file = os.path.join(filestore, os.path.basename(key))
    logging.debug("Bucket: {} {}".format(bucket_name, key))

    # download the cloudtrail json.gz file
    s3 = session.resource("s3", region_name=region_name)
    bucket = s3.Bucket(bucket_name)
    bucket.download_file(key, local_file)

    file = gzip.open(local_file, "r")
    records = json.loads(file.read().decode("utf-8"))["Records"]
    for record in records:
        if "errorMessage" in record:
            if record["errorMessage"] == "Failed authentication":
                print(
                    "Authentication failed username ",
                    record["userIdentity"]["userName"],
                    "from the ip address ",
                    record["sourceIPAddress"],
                )
                break

        if record["eventName"] in ["StartInstances", "StopInstances"]:
            ret_records[record["eventID"]] = record
            print(ret_records[record["eventID"]])

    # close and delete the CloudTrail json.gz file
    file.close()
    os.remove(local_file)

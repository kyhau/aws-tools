import hashlib
import os
import time

import boto3

WAIT_TIME_IN_SEC = 60
MAX_ATTEMPTS = 12


def handler(event: dict, context: dict):
    """
    This function handles the S3 events resulting from a new `PutObject` event corresponding to a file upload

    Parameters
    ----------
    event : Event details
    context : Extra event context
    """
    # Instruct the KB to start the ingestion job
    client = boto3.client("bedrock-agent")
    client_token = hashlib.sha256(
        event["Records"][0]["responseElements"]["x-amz-request-id"].encode()
    ).hexdigest()

    data_source_id = os.environ["DATA_SOURCE_ID"]
    kb_id = os.environ["KNOWLEDGE_BASE_ID"]

    succeeded = False
    attempt = 0
    while not succeeded and attempt < MAX_ATTEMPTS:
        attempt += 1
        try:
            print(f"CheckPt-{attempt}: dataSourceId={data_source_id}, knowledgeBaseId={kb_id}")
            resp = client.start_ingestion_job(
                clientToken=client_token,
                dataSourceId=data_source_id,
                knowledgeBaseId=kb_id,
                description="S3-originated data sync event",
            )
            succeeded = True
            print(f"CheckPt-{attempt}-resp: {resp}")
        except client.exceptions.ConflictException as e:
            print(f"ConflictException: dataSourceId={data_source_id}, knowledgeBaseId={kb_id}")
            print(e)
            time.sleep(WAIT_TIME_IN_SEC)

    if attempt == MAX_ATTEMPTS and not succeeded:
        raise Exception("Exceeded maximum attempts")

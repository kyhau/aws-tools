import boto3
import json
import logging
import os
import uuid

LOG = logging.getLogger()
LOG.setLevel(logging.INFO)


def main(event, context):
    LOG.info(f"Event: {json.dumps(event)}")
    
    query_string_params = event["queryStringParameters"]
    if query_string_params is not None:
        target_url = query_string_params["targetUrl"]
        if target_url is not None:
            return create_short_url(event)

    path_params = event["pathParameters"]
    if path_params is not None and path_params["proxy"] is not None:
        return read_short_url(event)

    return {
        "statusCode": 200,
        "body": "usage: ?targetUrl=URL"
    }


def create_short_url(event):
    table_name = os.environ.get("TABLE_NAME")
    
    target_url = event["queryStringParameters"]["targetUrl"]
    id = str(uuid.uuid4())[0:8]
    
    table = boto3.resource("dynamodb").Table(table_name)
    table.put_item(Item={
        "id": id,
        "target_url": target_url,
    })
    
    url = f'https://{event["requestContext"]["domainName"]}{event["requestContext"]["path"]}{id}'
    
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/plain"},
        "body": f"Created URL: {url}"
    }


def read_short_url(event):
    # Parse redirect ID from path
    id = event["pathParameters"]["proxy"]
    table_name = os.environ.get("TABLE_NAME")

    table = boto3.resource("dynamodb").Table(table_name)
    resp = table.get_item(Key={"id": id})
    LOG.debug(f"Response: {resp}")
    
    item = resp.get("Item")
    if item is None:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "text/plain"},
            "body": f"No redirect found for {id}"
        }
    
    return {
        "statusCode": 301,
        "headers": {
            "location": item.get("target_url")
        }
    }
import json
import urllib.parse
from os import environ

import requests

# from aws_xray_sdk.core import patch_all, xray_recorder
# patch_all()

HEADERS = {"X-Aws-Parameters-Secrets-Token": environ.get("AWS_SESSION_TOKEN")}
SECRET_NAME = "MyTestSecret"
SECRET_PORT = environ.get("PARAMETERS_SECRETS_EXTENSION_HTTP_PORT")


def get_lambda_response(status_code: int, body: str):
    return {
        "statusCode": status_code,
        "body": body
    }


def get_secret(secret_id: str, version_stage: str=None) -> str:
    request_uri = f"http://localhost:{SECRET_PORT}/secretsmanager/get?secretId={urllib.parse.quote(secret_id)}"
    if version_stage:
        request_uri = f"{request_uri}&versionStage={urllib.parse.quote(version_stage)}"

    response = requests.get(url=request_uri, headers=HEADERS)
    return response.json()["SecretString"]


def lambda_handler(event, context):
    # print(f"Testing - Retrieved value: {get_secret(secret_id=SECRET_NAME)}")
    return get_lambda_response(200, json.dumps("Hello from Lambda!"))

import json

import boto3

bedrock_client = boto3.client("bedrock")
response = bedrock_client.list_foundation_models()

for model in response["modelSummaries"]:
    print(json.dumps(model, indent=2))

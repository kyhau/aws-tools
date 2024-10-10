"""
This script supports 2 Bedrock modes:
1. Using Bedrock Agent (default mode) - see BedrockAgentHelper
2. Using Bedrock Models (direct invoke-model without using Bedrock Agent) - see BedrockRuntimeHelper
"""
import base64
import json
import logging
import os

import boto3
import urllib3
from botocore.exceptions import ClientError

logging.getLogger().setLevel(logging.INFO)
logging.getLogger("botocore").setLevel(logging.CRITICAL)
logging.getLogger("boto3").setLevel(logging.CRITICAL)
logging.getLogger("urllib3.connectionpool").setLevel(logging.CRITICAL)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

IS_AWS_SAM_LOCAL = os.environ.get("AWS_SAM_LOCAL") == "true"

http = urllib3.PoolManager()

# Bedrock Agent settings
AGENT_ID = os.environ.get("AgentId")
AGENT_ALIAS_ID = os.environ.get("AgentAliasId")
INVOKE_AGENT_ATTEMPTS = 3

# Bedrock Models (direct invoke-model without using Bedrock Agent)
GENERATE_IMAGE_KEYWORD = "image:"
IMAGE_MODEL_ID = os.environ.get("ImageModelId")
IMAGE_MODEL_REGION = "us-east-1"  # US East (N. Virginia)
TEXT_CHAT_MODEL_ID = os.environ.get("TextChatModelId")


class Messenger:
    def __init__(self, session_id: str):
        self.session_id = session_id

    def call_chat_post(self, message):
        print(message)

    def call_file_upload(self, image_bytes, user):
        print(f"Image upload: {image_bytes} to {user}")


class BedrockAgentHelper:
    REF_LOCATIONS = {
        "CONFLUENCE": "confluenceLocation",
        "S3": "s3Location",
        "SALESFORCE": "salesforceLocation",
        "SHAREPOINT": "sharePointLocation",
        "WEB": "webLocation",
    }

    def __init__(self, messenger: Messenger):
        self.messenger = messenger
        self.session_id = messenger.session_id
        self.references = []

    def parse_citations(self, citations: list):
        try:
            logging.info(f"Citations: {citations}")
            for cite in citations:
                for ref in cite["retrievedReferences"]:
                    self.references.append(
                        (
                            ref["location"]["type"],
                            ref["location"][self.REF_LOCATIONS[ref["location"]["type"]]]["uri"],
                        )
                    )
        except Exception as e:
            logging.exception(e)

    def respond_with_agent(self, message: str):
        """Process user message using the given Bedrock Agent"""
        agents_runtime = boto3.client("bedrock-agent-runtime")

        for _ in range(INVOKE_AGENT_ATTEMPTS):
            response = agents_runtime.invoke_agent(
                agentId=AGENT_ID,
                agentAliasId=AGENT_ALIAS_ID,
                sessionId=self.session_id,
                inputText=message,
                endSession=False,
                enableTrace=False,
                # memoryId  # TODO The unique identifier of the agent memory
            )
            completion = ""
            try:
                logging.info(
                    f"sessionId={response.get('sessionId')}, memoryId={response.get('memoryId')}"
                )
                for event in response.get("completion"):
                    chunk = event["chunk"]
                    completion = completion + chunk["bytes"].decode()
                    logging.info(f"Completion: {completion}")

                    self.parse_citations(chunk.get("attribution", {}).get("citations", []))

                if len(completion) == 0:
                    self.messenger.call_chat_post("Let me think...")
                    continue

            except ClientError as e:
                logging.exception(e)
                self.messenger.call_chat_post("Let me think...")
                continue
            except KeyError as e:
                logging.exception(e)
                self.messenger.call_chat_post("Let me think...")
                continue

            completion += self.format_references()

            self.messenger.call_chat_post(completion)
            return

        self.messenger.call_chat_post("I am sorry, I cannot find that information.")


class BedrockRuntimeHelper:
    def __init__(self, messenger: Messenger):
        self.messenger = messenger
        self.session_id = messenger.session_id

    def respond_with_model_for_image(self, message: str, user: str):
        """Process user message using the given Bedrock model (without agent)"""
        bedrock_runtime = boto3.client("bedrock-runtime", region_name=IMAGE_MODEL_REGION)

        body = json.dumps(
            {
                "taskType": "TEXT_IMAGE",
                "textToImageParams": {
                    "text": message,
                    # "negativeText": "",
                },
                "imageGenerationConfig": {
                    "numberOfImages": 1,
                    "height": 768,
                    "width": 768,
                    "cfgScale": 5.0,  # 1.1 - 10.0; the lower the value the more randomness
                },
            }
        )

        try:
            response = bedrock_runtime.invoke_model(
                body=body,
                contentType="application/json",
                accept="application/json",
                modelId=IMAGE_MODEL_ID,
            )
            response_body = json.loads(response.get("body").read())
        except Exception as e:
            self.messenger.call_chat_post(
                f"I am sorry, I am unable to generate an image. {e.response['Error']['Message']}"
            )
            logging.exception(e)
            return

        finish_reason = response_body.get("error")
        if finish_reason is not None:
            self.messenger.call_chat_post(
                "I am sorry, I am unable to generate an image at the moment. Please try again later."
            )
            logging.error(f"Image generation error. Error: {finish_reason}")
            return

        base64_image = response_body.get("images")[0]
        base64_bytes = base64_image.encode("ascii")
        image_bytes = base64.b64decode(base64_bytes)
        self.messenger.call_file_upload(image_bytes, user)


def lambda_handler(event, context) -> dict:
    if AGENT_ID is None or AGENT_ALIAS_ID is None:
        return {
            "statusCode": 500,
            "body": "Bedrock Agent ID and Alias ID are not set. Please set them in the environment variables.",
        }

    logging.info(f"Received: {event}")

    text_msg = event.get("message")
    session_id = event.get("session_id")
    user = event.get("user_id")

    messenger = Messenger(session_id=session_id)

    if text_msg:
        if text_msg.lower().startswith(GENERATE_IMAGE_KEYWORD):
            new_text_msg = text_msg[len(GENERATE_IMAGE_KEYWORD):].strip()
            BedrockRuntimeHelper(messenger).respond_with_model_for_image(new_text_msg, user)
        else:
            BedrockAgentHelper(messenger).respond_with_agent(text_msg)
    else:
        messenger.call_chat_post("How are you doing?")

    return {
        "statusCode": 200,
        "body": "OK",
    }


def main():
    lambda_handler(
        event={
            "message": "What is the capital of France?",
            "session_id": "123",
            "user_id": "MrJenkins",
        },
        context=None,
    )


if __name__ == "__main__":
    main()

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Shows how to send an document as part of a message to Anthropic Claude 3 Sonnet (on demand).
Source: https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html
"""

import logging

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def generate_message(bedrock_client, model_id, input_text, input_document):
    """
    Sends a message to a model.
    Args:
        bedrock_client: The Boto3 Bedrock runtime client.
        model_id (str): The model ID to use.
        input text : The input message.
        input_document : The input document.

    Returns:
        response (JSON): The conversation that the model generated.

    """

    logger.info("Generating message with model %s", model_id)

    # Message to send.

    message = {
        "role": "user",
        "content": [
            {"text": input_text},
            {
                "document": {
                    "name": "MyDocument",
                    "format": "txt",
                    "source": {"bytes": input_document},
                }
            },
        ],
    }

    messages = [message]

    # Send the message.
    response = bedrock_client.converse(modelId=model_id, messages=messages)

    return response


def main():
    """
    Entrypoint for Anthropic Claude 3 Sonnet example.
    """

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
    input_text = "What's in this document?"
    input_document = "path/to/document.pdf"

    try:
        bedrock_client = boto3.client(service_name="bedrock-runtime")

        response = generate_message(bedrock_client, model_id, input_text, input_document)

        output_message = response["output"]["message"]

        print(f"Role: {output_message['role']}")

        for content in output_message["content"]:
            print(f"Text: {content['text']}")

        token_usage = response["usage"]
        print(f"Input tokens:  {token_usage['inputTokens']}")
        print(f"Output tokens:  {token_usage['outputTokens']}")
        print(f"Total tokens:  {token_usage['totalTokens']}")
        print(f"Stop reason: {response['stopReason']}")

    except ClientError as err:
        message = err.response["Error"]["Message"]
        logger.error("A client error occurred: %s", message)
        print(f"A client error occured: {message}")

    else:
        print(f"Finished generating text with model {model_id}.")


if __name__ == "__main__":
    main()

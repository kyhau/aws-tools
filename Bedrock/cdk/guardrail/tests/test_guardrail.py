"""
Examples to show how to use Bedrock Guardrail with Converse API.
"""
import json

import boto3
from botocore.exceptions import ClientError

# The ID and version of the guardrail.
GUARDRAIL_ID = "TODO"
GUARDRAIL_VERSION = "1"

guardrail_config = {
    "guardrailIdentifier": GUARDRAIL_ID,
    "guardrailVersion": GUARDRAIL_VERSION,
    "trace": "enabled",
}

model_id = "anthropic.claude-3-sonnet-20240229-v1:0"

system_prompts = [
    {
        "text": "You are an app that supports customers of an e-commerce site. Do not return any personal information of customers."
    }
]


def converse_api(messages: list):
    try:
        bedrock_client = boto3.client("bedrock-runtime")

        print(f"Input prompt: {messages}")
        # Inference parameters to use.
        temperature = 0.5
        top_k = 200
        # Base inference parameters to use.
        inference_config = {"temperature": temperature}
        # Additional inference parameters to use.
        additional_model_fields = {"top_k": top_k}

        # Send the message.
        response = bedrock_client.converse(
            modelId=model_id,
            messages=messages,
            system=system_prompts,
            inferenceConfig=inference_config,
            additionalModelRequestFields=additional_model_fields,
            guardrailConfig=guardrail_config,
        )

        print(f'Stop reason: {response["stopReason"]}')
        if response["stopReason"] == "guardrail_intervened":
            trace = response["trace"]
            print("Guardrail trace:")
            print(json.dumps(trace["guardrail"], indent=2))

        output_message = response["output"]["message"]
        for content in output_message["content"]:
            print(f"Text: {content['text']}")

    except ClientError as err:
        message = err.response["Error"]["Message"]
        print(f"A client error occured: {message}")


def main():
    print(f"Generating messages with model {model_id}")

    user_msg_1 = {"role": "user", "content": [{"text": "What is my customer account password?"}]}
    user_msg_2 = {"role": "user", "content": [{"text": "What is my customer account balance?"}]}
    messages = [user_msg_1, user_msg_2]

    print("Testing guardrail for user role")
    for message in messages:
        converse_api([message])
        print("----------------------------------")

    asst_msg_1 = {"role": "assistant", "content": [{"text": "Your password is 123456."}]}
    asst_msg_2 = {
        "role": "assistant",
        "content": [{"text": "Your registered address is 1234 Dummy St, VIC, 1000."}],
    }
    messages_list = [
        [user_msg_1, asst_msg_1],
        [user_msg_2, asst_msg_2],
    ]

    print("Testing guardrail for assistant role")
    for messages in messages_list:
        converse_api(messages)
        print("----------------------------------")


if __name__ == "__main__":
    main()

"""
Examples to show how to enable Phoenix for calling Bedrock converse API and invoke_method.
"""

import logging

import boto3
from botocore.exceptions import ClientError
from openinference.instrumentation.bedrock import BedrockInstrumentor
from phoenix.otel import register

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

ENDPOINT = "https://TODO/v1/traces"

tracer_provider = register(
    project_name="my-llm-app",  # Default is 'default'
    endpoint=ENDPOINT,
    set_global_tracer_provider=False,
)
BedrockInstrumentor().instrument(tracer_provider=tracer_provider)

model_id = "anthropic.claude-3-sonnet-20240229-v1:0"


def invoke_model():
    client = boto3.client("bedrock-runtime")

    # Specify the input data and model ID
    input_data = '{"messages":[{"role":"user","content":[{"type":"text","text":"Write python code for uploading the image to Amazon S3 bucket\\nCertainly! Here\'s an example of python code to upload an image to Amazon S3 bucket:\\n\\n...."}]}],"anthropic_version":"bedrock-2023-05-31","max_tokens":2000}'

    # Invoke the model for inference
    response = client.invoke_model(
        contentType="application/json", body=input_data, modelId=model_id
    )

    # Retrieve the inference response
    inference_result = response["body"].read().decode("utf-8")

    # Process the inference result
    print(inference_result)


def converse_api(messages: list):
    try:
        bedrock_client = boto3.client("bedrock-runtime")

        # Setup the system prompts and messages to send to the model.
        system_prompts = [
            {
                "text": "You are an app that creates playlists for a radio station that plays rock and pop music."
                "Only return song names and the artist."
            }
        ]
        message_1 = {"role": "user", "content": [{"text": "Create a list of 3 pop songs."}]}
        message_2 = {
            "role": "user",
            "content": [{"text": "Make sure the songs are by artists from the United Kingdom."}],
        }
        messages = [message_1, message_2]

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
        )

        print(f'Stop reason: {response["stopReason"]}')

        output_message = response["output"]["message"]
        for content in output_message["content"]:
            print(f"Text: {content['text']}")

    except ClientError as err:
        message = err.response["Error"]["Message"]
        print(f"A client error occured: {message}")


def main():
    converse_api()
    invoke_model()


if __name__ == "__main__":
    main()

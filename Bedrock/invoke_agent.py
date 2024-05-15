import os
import uuid

import boto3

AGENT_ID = os.getenv("AGENT_ID")
AGENT_ALIAS = os.getenv("AGENT_ALIAS")

# create a boto3 bedrock agent client
client = boto3.client("bedrock-agent-runtime")

# invoke the agent API
response = client.invoke_agent(
    inputText="show all open claims",
    agentId=AGENT_ID,
    agentAliasId=AGENT_ALIAS,
    sessionId=str(uuid.uuid1()),  # random identifier,
    enableTrace=True
)

print(response)

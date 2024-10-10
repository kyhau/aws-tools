from pathlib import Path

from aws_cdk import Stack
from backend.bedrock_aoss import AgentWithAOSSKB
from constructs import Construct

AGENT_PROMPT_FILE = Path(__file__).parents[2] / "resources" / "agent_prompt.txt"


class BedrockAgentStack(Stack):
    def __init__(self, scope: Construct, id: str, config: dict, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        app_name = config["AppName"]

        # Create the S3 Bucket + Agent + KB + Amazon OpenSearch Service (AOSS)
        # Optionally, you can deploy the AOSS resources separately
        AgentWithAOSSKB(
            scope=self,
            id=f"{app_name}-Bedrock",
            agent_instructions=AGENT_PROMPT_FILE.read_text(),
            agent_model_id=config["Bedrock"]["AgentModelId"],
            agent_alias_name=config["Bedrock"]["AgentAlias"],
            embeddings_model_id=config["Bedrock"]["EmbeddingsModelId"],
            embeddings_vector_size=config["Bedrock"]["EmbeddingsVectorSize"],
            log_retention_in_days=config["LogRetentionInDays"],
        )

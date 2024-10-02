from aws_cdk.aws_bedrock import CfnGuardrail, CfnGuardrailVersion
from aws_cdk import CfnOutput, Stack
from constructs import Construct


class BedrockGuardrailStack(Stack):
    def __init__(self, scope: Construct, id: str, config: dict, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.config = config
        app_name = self.config["AppName"].lower()

        params = {
            "blocked_input_messaging": self.config["BedrockGuardrail"]["blocked_input_messaging"],
            "blocked_outputs_messaging": self.config["BedrockGuardrail"][
                "blocked_outputs_messaging"
            ],
        }

        # (1) Content filter policies
        content_policy_config = self.create_content_policy_config()
        if content_policy_config:
            params["content_policy_config"] = content_policy_config

        # (2) Contextual grounding policies
        contextual_grounding_policy_config = self.create_contextual_grounding_policy_config()
        if contextual_grounding_policy_config:
            params["contextual_grounding_policy_config"] = contextual_grounding_policy_config

        # (3) Sensitive information policies
        sensitive_information_policy_config = self.create_sensitive_information_policy_config()
        if sensitive_information_policy_config:
            params["sensitive_information_policy_config"] = sensitive_information_policy_config

        # (4) Topic policies
        topic_policy_config = self.create_topic_policy_config()
        if topic_policy_config:
            params["topic_policy_config"] = topic_policy_config

        # (5) Word filters
        word_policy_config = self.create_word_policy_config()
        if word_policy_config:
            params["word_policy_config"] = word_policy_config

        guardrail = CfnGuardrail(
            self,
            id=f"{app_name}-guardrail",
            name=f"{app_name}-guardrail",
            description=f"{app_name} Guardrail",
            # kms_key_arn="kmsKeyArn", TODO
            **params,
        )

        guardrail_version = CfnGuardrailVersion(
            self,
            id=f"{app_name}-guardrail-version",
            description=f"{app_name} Guardrail Version",
            guardrail_identifier=guardrail.attr_guardrail_id,
        )
        CfnOutput(self, "GuardrailIdentifier", value=guardrail.attr_guardrail_id)
        CfnOutput(self, "GuardrailVersion", value=guardrail_version.attr_version)

    def create_content_policy_config(self) -> CfnGuardrail.ContentPolicyConfigProperty:
        """
        Adjust filter strengths to block input prompts or model responses containing harmful content.
        """
        filters_config = [
            CfnGuardrail.ContentFilterConfigProperty(
                input_strength=v["input_strength"],
                output_strength=v["output_strength"],
                type=k,
            )
            for k, v in self.config["BedrockGuardrail"]["content_policy_config"].items()
        ]
        return CfnGuardrail.ContentPolicyConfigProperty(filters_config=filters_config)

    def create_contextual_grounding_policy_config(
        self,
    ) -> CfnGuardrail.ContextualGroundingPolicyConfigProperty:
        """
        Use contextual grounding check to filter hallucinations in responses
        """
        if self.config["BedrockGuardrail"].get("contextual_grounding_policy_config"):
            filters_config = [
                CfnGuardrail.ContextualGroundingFilterConfigProperty(
                    threshold=v["threshold"],
                    type=k,
                )
                for k, v in self.config["BedrockGuardrail"][
                    "contextual_grounding_policy_config"
                ].items()
            ]
            return CfnGuardrail.ContextualGroundingPolicyConfigProperty(filters_config=filters_config)
        return None

    def create_sensitive_information_policy_config(
        self,
    ) -> CfnGuardrail.SensitiveInformationPolicyConfigProperty:
        """
        Block or mask sensitive information such as personally identifiable information (PII)
        or custom regex in user inputs and model responses.
        """
        params = {}
        pii_entities_config = [
            CfnGuardrail.PiiEntityConfigProperty(action=v, type=k)
            for k, v in self.config["BedrockGuardrail"]["sensitive_information_policy_config"][
                "pii_entities_config"
            ].items()
        ]
        if pii_entities_config:
            params["pii_entities_config"] = pii_entities_config

        regexes_config = [
            CfnGuardrail.RegexConfigProperty(
                action=item["action"],
                name=item["name"],
                pattern=item["pattern"],
                description=item.get("description", ""),
            )
            for item in self.config["BedrockGuardrail"]["sensitive_information_policy_config"][
                "regexes_config"
            ]
        ]
        if regexes_config:
            params["regexes_config"] = regexes_config

        if pii_entities_config or regexes_config:
            return CfnGuardrail.SensitiveInformationPolicyConfigProperty(**params)
        return None

    def create_topic_policy_config(self) -> CfnGuardrail.TopicPolicyConfigProperty:
        """
        Block denied topics to remove harmful content
        """
        topics_config = [
            CfnGuardrail.TopicConfigProperty(
                definition=item["definition"],
                name=item["name"],
                type="DENY",
                examples=item.get("examples", []),
            )
            for item in self.config["BedrockGuardrail"]["topic_policy_config"]
        ]
        if topics_config:
            return CfnGuardrail.TopicPolicyConfigProperty(topics_config=topics_config)
        return None

    def create_word_policy_config(self) -> CfnGuardrail.WordPolicyConfigProperty:
        """
        Configure filters to block undesirable words, phrases, and profanity. Such words can include offensive terms, competitor names etc.
        """
        params = {}

        managed_word_lists_config = (
            [CfnGuardrail.ManagedWordsConfigProperty(type="PROFANITY")]
            if self.config["BedrockGuardrail"]["word_policy_config"].get(
                "managed_word_lists_config"
            )
            == "PROFANITY"
            else []
        )
        if managed_word_lists_config:
            params["managed_word_lists_config"] = managed_word_lists_config

        words_config = [
            CfnGuardrail.WordConfigProperty(text=item)
            for item in self.config["BedrockGuardrail"]["word_policy_config"].get(
                "words_config", []
            )
        ]
        if words_config:
            params["words_config"] = words_config

        if managed_word_lists_config or words_config:
            return CfnGuardrail.WordPolicyConfigProperty(**params)
        return None

import os

from aws_cdk import CfnOutput, SecretValue, Stack
from aws_cdk import aws_iam as iam
from aws_cdk import aws_secretsmanager as sm
from constructs import Construct
from lib.kms import create_kms_key_and_alias


class SecretsStack(Stack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        app_name: str,
        secrets: dict,
        is_single_object_secret: bool,
        key_admin_arn_list: list,
        key_user_arn_pattern_list: list,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)

        key_admin_arns = [
            iam.Role.from_role_arn(self, arn_str.split("/")[-1], arn_str)
            for arn_str in key_admin_arn_list
        ]

        key_alias_name = f"alias/{app_name.lower()}"

        key_alias = create_kms_key_and_alias(
            self,
            id="KmsKey",
            key_alias=key_alias_name,
            key_admin_arns=key_admin_arns,
            key_user_arns=key_user_arn_pattern_list,
        )

        app_secrets = {}
        if is_single_object_secret is True:
            sm_secret_name = f"/apps/{app_name}/secrets".lower()
            sm_secret = self.create_secret_with_object(
                sm_secret_name=sm_secret_name,
                description=f"Secrets of {app_name}",
                secrets=secrets,
                key_alias=key_alias,
            )
            app_secrets[app_name.replace("_", "-").lower()] = sm_secret
        else:
            for secret_name, item in secrets.items():
                sm_secret_name = f"/apps/{app_name}/{secret_name}".lower()
                sm_secret = self.create_secret_with_single_value(
                    sm_secret_name=sm_secret_name,
                    description=item.get("description", ""),
                    secret_value=item["value"],
                    key_alias=key_alias,
                )
                app_secrets[f"{app_name}-{secret_name}".replace("_", "-").lower()] = sm_secret

        policy_statement = self.create_secrets_policy_statement(
            key_user_arns_patterns=key_user_arn_pattern_list
        )

        for secret_name, sm_secret in app_secrets.items():
            sm_secret.add_to_resource_policy(policy_statement)
            sm_secret.node.add_dependency(key_alias)

            CfnOutput(
                scope=self,
                id=f"{secret_name}-secret-arn",
                value=sm_secret.secret_arn,
                description=f"ARN of Secrets Manager secret {secret_name}",
                export_name=f"{secret_name}-secret-arn",
            )

        CfnOutput(
            scope=self,
            id=f"{app_name}-secret-kms-alias-arn",
            value=key_alias.alias_arn,
            description="ARN of KMS key alias used to encrypt app secrets in Secrets Manager",
            export_name=f"{app_name}-secret-kms-alias-arn",
        )

    def create_secret_with_object(
        self, sm_secret_name: str, description: str, secrets: dict, key_alias: str
    ) -> sm.Secret:
        return sm.Secret(
            self,
            id=sm_secret_name.replace("/", "-").lower(),
            description=f"Secrets for app {app_name}",
            encryption_key=key_alias,
            secret_name=secret_name,
            secret_object_value={
                secret["Name"]: SecretValue.unsafe_plain_text(secret["Value"]) for secret in secrets
            },
        )

    def create_secret_with_single_value(
        self, sm_secret_name: str, description: str, secret_value: str, key_alias: str
    ) -> sm.Secret:
        return sm.Secret(
            self,
            id=sm_secret_name.replace("/", "-").lower(),
            description=description,
            encryption_key=key_alias,
            secret_name=sm_secret_name,
            secret_string_value=SecretValue.unsafe_plain_text(secret_value),
        )

    def create_secrets_policy_statement(self, key_user_arns_patterns: list) -> iam.PolicyStatement:
        return iam.PolicyStatement(
            actions=["secretsmanager:GetSecretValue"],
            conditions={"ArnLike": {"aws:PrincipalArn": key_user_arns_patterns}},
            effect=iam.Effect.ALLOW,
            principals=[iam.AnyPrincipal()],
            resources=["*"],
        )

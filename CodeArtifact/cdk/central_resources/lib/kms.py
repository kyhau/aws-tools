from aws_cdk import (
    aws_iam,
    aws_kms,
)
from constructs import (
    Construct,
)


def create_kms_key_and_alias(
    scope: Construct,
    construct_id: str,
    key_alias: str,
    key_admin_arns,
) -> aws_kms.Key:
    policy_document = aws_iam.PolicyDocument(
        statements=[
            aws_iam.PolicyStatement(
                actions=["kms:*"],
                principals=[aws_iam.AccountRootPrincipal()],
                resources=["*"],
                sid="EnableIAMUserPermissions",
            ),
            aws_iam.PolicyStatement(
                actions=[
                    "kms:Create*",
                    "kms:Describe*",
                    "kms:Enable*",
                    "kms:List*",
                    "kms:Put*",
                    "kms:Update*",
                    "kms:Revoke*",
                    "kms:Disable*",
                    "kms:Get*",
                    "kms:Delete*",
                    "kms:TagResource",
                    "kms:UntagResource",
                    "kms:ScheduleKeyDeletion",
                    "kms:CancelKeyDeletion",
                ],
                principals=key_admin_arns,
                resources=["*"],
                sid="AllowAccessForKeyAdministrators",
            ),
        ]
    )

    key = aws_kms.Key(
        scope,
        construct_id,
        enable_key_rotation=True,
        policy=policy_document,
    )
    return aws_kms.Alias(
        scope,
        f"{construct_id}Alias",
        alias_name=key_alias,
        target_key=key,
    )

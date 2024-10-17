from aws_cdk import aws_iam as iam
from aws_cdk import aws_kms as kms
from constructs import Construct


def create_kms_key_and_alias(
    scope: Construct,
    id: str,
    key_alias: str,
    key_admin_arns: list,
    key_user_arns_like: list,
    enable_key_rotation: bool = False,
) -> kms.Key:
    policy_document = iam.PolicyDocument(
        statements=[
            iam.PolicyStatement(
                actions=["kms:*"],
                principals=[iam.AccountRootPrincipal()],
                resources=["*"],
                sid="EnableIAMUserPermissions",
            ),
            iam.PolicyStatement(
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
                principals=[
                    iam.Role.from_role_arn(scope, arn_str.split("/")[-1], arn_str)
                    for arn_str in key_admin_arns
                ],
                resources=["*"],
                sid="AllowAccessForKeyAdministrators",
            ),
            iam.PolicyStatement(
                actions=["kms:Decrypt"],
                conditions={"ArnLike": {"aws:PrincipalArn": key_user_arns_like}},
                principals=[iam.AnyPrincipal()],
                resources=["*"],
                sid="AllowDecrypt",
            ),
        ]
    )

    key = kms.Key(scope, id, enable_key_rotation=enable_key_rotation, policy=policy_document)

    return kms.Alias(scope, f"{id}Alias", alias_name=key_alias, target_key=key)

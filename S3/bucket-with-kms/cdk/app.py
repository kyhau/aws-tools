#!/usr/bin/env python3
from aws_cdk import aws_iam, aws_kms, aws_s3, core

# - Create KMS key, alias and key policy
# - Create a bucket
# - Create policy for accessing the bucket


env = {
    "app_name": "todo",
    "bucket_name": "todo",
    "rw_role_arns": [
        "arn:aws:iam::111122223333:role/rw-role",
    ],
    "key_admin_arn": "arn:aws:iam::111122223333:role/key-admin",
}
alias_name=f'alias/{env["bucket_name"]}-kms'


class S3BackupStack(core.Stack):    
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        env = kwargs.get("env")
        key_admin_role = aws_iam.Role.from_role_arn(self, "key_admin_role", env["key_admin_arn"])

        key = aws_kms.Key(self, f'{env["app_name"]}KmsKey', enable_key_rotation=True)

        key.add_alias(alias_name)
        
        # Allow administration of the key
        key.add_to_resource_policy(
            aws_iam.PolicyStatement(
                actions= [
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
                    "kms:ScheduleKeyDeletion",
                    "kms:CancelKeyDeletion",
                    "kms:GenerateDataKey",
                ],
                principals= [key_admin_role],
                resources=["*"]))

        # Allow use of the key
        key.add_to_resource_policy(
            aws_iam.PolicyStatement(
                actions= [
                    "kms:Decrypt",
                    "kms:DescribeKey",
                    "kms:Encrypt",
                    "kms:GenerateDataKey*",
                    "kms:ReEncrypt*",
                ],
                principals= [key_admin_role],
                resources=["*"]))
        
        bucket = aws_s3.Bucket(
            self, f'{env["app_name"]}Bucket',
            bucket_name=env["bucket_name"],
            block_public_access=aws_s3.BlockPublicAccess.BLOCK_ALL,
            encryption=aws_s3.BucketEncryption.KMS,
            encryption_key=key,
            removal_policy=core.RemovalPolicy.RETAIN,
        )
        
        for rw_role_arn in env["rw_role_arns"]:
            rw_role = aws_iam.Role.from_role_arn(self, rw_role_arn.split("/")[-1], rw_role_arn)
            bucket.grant_read_write(rw_role)

        core.CfnOutput(self, "BucketName", value=bucket.bucket_name)

        core.CfnOutput(
            self, "KeyAliasArn",
            value=core.Fn.sub("arn:aws:kms:${AWS::Region}:${AWS::AccountId}:" + alias_name))


app = core.App()
S3BackupStack(app, "bucket-with-kms", env=env)
app.synth()

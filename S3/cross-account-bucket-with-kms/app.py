from aws_cdk import (
    aws_iam as iam,
    aws_kms as kms,
    aws_s3 as s3,
    core,
)

"""
1. KMS at account A
2. Bucket at account A
3. BucketPolicy at account A
4. KMS policy at account A
5. IAM policy at other account(s)
"""

settings = {
    "app_name": "k-demo",
    "bucket_name": "k-shared-bucket",
    "kms_name": "",
    "roles_to_read": [],
    "roles_to_write": [],
}


class CrossAccountS3Stack(core.Stack):
    def __init__(self, app: core.App, id: str, settings: str) -> None:
        super().__init__(app, id)

        # TODO
        kms_key = kms.Key(
            self,
            f"{settings['app_name']}-KMS-Key",
            description="",
            enable_key_rotation=True,
            policy=None,  # TODO A policy document with permissions for the account root to administer the key will be created.
        )

        bucket = s3.Bucket(
            self,
            f"{settings['app_name']}-CrossAccountS3Stack",
            block_public_access=True,
            bucket_name=settings.get("bucket_name"),
            encryption=s3.BucketEncryption.KMS,
            encryption_key=None,
            removal_policy=core.RemovalPolicy.RETAIN,
            versioned=False,
        )

        policy_statement_1 = iam.PolicyStatement(effect = iam.Effect.ALLOW)
        policy_statement_1.add_resources([
            bucket.bucketArn,
            f"{bucket.bucketArn}/*",
        ])
        policy_statement_1.add_actions([
            "s3:GetObject",
            "s3:ListBucket",
        ])
        policy_statement_1.add_arn_principal("arn:aws:iam:::role/Bob’s_Data_Access_Role")

        bucket_policy = s3.BucketPolicy(self, "BucketPolicy", bucket)
        bucket_policy.document = iam.PolicyDocument(
            statements = [policy_statement_1])


def main():
    app = core.App()
    CrossAccountS3Stack(app, "CrossAccountS3Example", settings.get("bucket_name"))
    app.synth()


if __name__ == "__main__": main()

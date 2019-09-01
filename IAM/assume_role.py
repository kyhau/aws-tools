import boto3

ROLE_ARN = "arn:aws:iam::account-of-role-to-assume:role/name-of-role"


def get_temp_credentials(role_arn):
    # The calls to AWS STS AssumeRole must be signed with the access key ID
    # and secret access key of an existing IAM user or by using existing temporary
    # credentials such as those from another role. (You cannot call AssumeRole
    # with the access key for the root account.) The credentials can be in
    # environment variables or in a configuration file and will be discovered
    # automatically by the boto3.client() function. For more information, see the
    # Python SDK documentation:
    # http://boto3.readthedocs.io/en/latest/reference/services/sts.html#client

    # create an STS client object that represents a live connection to the
    # STS service
    sts_client = boto3.client("sts")

    # Call the assume_role method of the STSConnection object and pass the role
    # ARN and a role session name.
    assumed_role_object=sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName="AssumeRoleSession1",
        DurationSeconds=3600,  # 15 mins to 1 hour or 12 hours
    )

    # From the response that contains the assumed role, get the temporary
    # credentials that can be used to make subsequent API calls
    return assumed_role_object["Credentials"]


credentials = get_temp_credentials(role_arn=ROLE_ARN)

# Use the temporary credentials that AssumeRole returns to make a
# connection to Amazon S3
s3_resource = boto3.resource(
    "s3",
    aws_access_key_id=credentials["AccessKeyId"],
    aws_secret_access_key=credentials["SecretAccessKey"],
    aws_session_token=credentials["SessionToken"],
)

# Use the Amazon S3 resource object that is now configured with the
# credentials to access your S3 buckets.
for bucket in s3_resource.buckets.all():
    print(bucket.name)
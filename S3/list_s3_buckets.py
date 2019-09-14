import boto3
from boto3.session import Session

ROLE_ARN = "arn:aws:iam::210954854504:role/DEV-01"


def assume_role(role_arn, session_name="AssumeRoleSession1", duration_secs=3600):
    """aws sts assume-role --role-arn arn:aws:iam::00000000000000:role/example-role --role-session-name example-role"""

    resp = boto3.client("sts").assume_role(
        RoleArn=role_arn,
        RoleSessionName=session_name,
        DurationSeconds=duration_secs,  # 15 mins to 1 hour or 12 hours
    )
    return Session(
        aws_access_key_id=resp["Credentials"]["AccessKeyId"],
        aws_secret_access_key=resp["Credentials"]["SecretAccessKey"],
        aws_session_token=resp["Credentials"]["SessionToken"]
    )


# Either Start from a role ARN, or from a profile_name
#session = assume_role(ROLE_ARN)
session = Session(profile_name="TODO")

s3_resource = session.resource("s3")
for bucket in s3_resource.buckets.all():
    print(bucket.name)

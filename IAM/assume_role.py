import boto3
from boto3.session import Session


def assume_role(role_arn, session_name="AssumeRoleSession1", duration_secs=3600):
    """aws sts assume-role --role-arn arn:aws:iam::00000000000000:role/example-role --role-session-name example-role"""

    resp = boto3.client("sts").assume_role(
        RoleArn=role_arn,
        RoleSessionName=session_name,
        DurationSeconds=duration_secs)  # 15 mins to 1 hour or 12 hours

    return Session(
        aws_access_key_id=resp["Credentials"]["AccessKeyId"],
        aws_secret_access_key=resp["Credentials"]["SecretAccessKey"],
        aws_session_token=resp["Credentials"]["SessionToken"])


def test_assume_role_print_account_id(role_arn):
    session = assume_role(role_arn)
    client = session.client('sts')
    account_id = client.get_caller_identity()["Account"]
    print(account_id)

#test_assume_role_print_account_id(role_arn)
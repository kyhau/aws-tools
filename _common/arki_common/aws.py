import boto3
from boto3.session import Session
from os.path import exists

DEFAULT_ROLE_ARNS_FILE = "role_arns.txt"


def assume_role(role_arn, session_name="AssumeRoleSession1", duration_secs=3600):
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


def read_role_arns_from_file(filename=DEFAULT_ROLE_ARNS_FILE):
    if exists(filename):
        with open(filename) as f:
            lns = f.readlines()
            return [x.strip() for x in lns if x.strip() and not x.strip().startswith("#")] # ignore empty/commented line
    return []

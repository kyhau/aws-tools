import boto3
from boto3.session import Session
from os.path import exists

DEFAULT_ROLE_ARNS_FILE = "role_arns.txt"

account_ids_checked = []


def list_action(session):
    account_id = session.client("sts").get_caller_identity()["Account"]
    if account_id not in account_ids_checked:
        account_ids_checked.append(account_id)

        for bucket in session.resource("s3").buckets.all():
            print(f"{account_id}: {bucket.name}")


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


def read_role_arns_from_file():
    if exists(DEFAULT_ROLE_ARNS_FILE):
        with open(DEFAULT_ROLE_ARNS_FILE) as f:
            lns = f.readlines()
            return [x.strip() for x in lns if x.strip() and not x.strip().startswith("#")] # ignore empty/commented line
    return []


################################################################################
# Entry point

def main():
    # TODO Optional specify a profile instead
    # PROFILE_NAME = "default"
    PROFILE_NAME = None
    if PROFILE_NAME is not None:
        session = Session(profile_name=PROFILE_NAME)
        list_action(session)

    for role_arn in read_role_arns_from_file():
        session = assume_role(role_arn=role_arn)
        list_action(session)


if __name__== "__main__": main()

"""
List users
"""
from boto3.session import Session
import click

from arki_common.aws import assume_role, read_role_arns_from_file, DEFAULT_ROLE_ARNS_FILE


def list_action(session, results):
    try:
        paginator = session.client("iam").get_paginator("list_users")
        for page in paginator.paginate():
            for user in page["Users"]:
                results[user["Arn"]] = user
    except Exception as e:
        print(e)


################################################################################
# Entry point

@click.command()
@click.option("--profile", "-p", help="AWS profile name")
def main(profile):
    results = {}   # { user_arn: {data}, }

    if profile is not None:
        session = Session(profile_name=profile)
        list_action(session, results)

    for role_arn in read_role_arns_from_file(filename=DEFAULT_ROLE_ARNS_FILE):
        session = assume_role(role_arn=role_arn)
        list_action(session, results)

    print("UserArn, PasswordLastUsed")
    for user_arn, data in results.items():
        print(f"{user_arn}, {data.get('PasswordLastUsed')}")


if __name__ == "__main__": main()

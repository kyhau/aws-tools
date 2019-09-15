from boto3.session import Session
import click

from arki_common.aws import assume_role, read_role_arns_from_file, DEFAULT_ROLE_ARNS_FILE


def list_action(session, results):
    account_id = session.client("sts").get_caller_identity()["Account"]
    if account_id in results:
        return

    for bucket in session.resource("s3").buckets.all():
        results[account_id] = bucket.name


################################################################################
# Entry point

@click.command()
@click.option("--profile", "-p", help="AWS profile name")
def main(profile):
    results = {}    # { account_id: bucket_name }

    if profile is not None:
        session = Session(profile_name=profile)
        list_action(session, results)

    for role_arn in read_role_arns_from_file(filename=DEFAULT_ROLE_ARNS_FILE):
        session = assume_role(role_arn=role_arn)
        list_action(session, results)

    for account_id, bucket_name in results.items():
        print(f"{account_id}, {bucket_name}")


if __name__ == "__main__": main()

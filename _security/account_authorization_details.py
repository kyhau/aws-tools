from boto3.session import Session
import click

from arki_common.utils import print_json


@click.command()
@click.option("--profile", "-p", default="default", help="AWS profile name")
def main(profile):
    session = Session(profile_name=profile)
    paginator = session.client("iam").get_paginator("get_account_authorization_details")
    for page in paginator.paginate(): # Filter=['User'|'Role'|'Group'|'LocalManagedPolicy'|'AWSManagedPolicy']
        print_json(page)


if __name__ == "__main__": main()

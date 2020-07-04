"""
Print authorization details of User, Role, Group, LocalManagedPolicy, and/or AWSManagedPolicy in account(s).
"""
import click
import logging
import yaml
from arki_common.aws import AwsApiHelper

logging.getLogger().setLevel(logging.DEBUG)

CHOICES = ["User", "Role", "Group", "LocalManagedPolicy", "AWSManagedPolicy"]


class Helper(AwsApiHelper):
    def process_request(self, session, account_id, region, kwargs):
        paginator = session.client("iam").get_paginator("get_account_authorization_details")
        for page in paginator.paginate(**kwargs):
            for k, v in page.items():
                if v and k not in ["ResponseMetadata", "IsTruncated"]:
                    print(yaml.dump(page[k]))


@click.command()
@click.option("--filter", "-f", type=click.Choice(CHOICES, case_sensitive=False))
@click.option("--profile", "-p", help="AWS profile name. Use profiles in ~/.aws if not specified.")
def main(filter, profile):
    kwargs = {"Filter": [filter]} if filter else {}
    Helper().start(profile, "ap-southeast-2", "iam", kwargs)


if __name__ == "__main__":
    main()

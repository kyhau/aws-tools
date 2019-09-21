"""
Decode EC2's UserData
"""
import base64
from boto3.session import Session
import click
from collections import defaultdict
import json
import logging
from os.path import basename

from arki_common.aws import assume_role, read_role_arns_from_file, DEFAULT_ROLE_ARNS_FILE
from arki_common import init_logging


APP_NAME = basename(__file__).split(".")[0]
DEFAULT_SESSION_NAME = "AssumeRoleSession-ListIamUsers-local"
OUTPUT_FILE = f"{APP_NAME}.json"
LOG_FILE = None    # or LOG_FILE = f"{APP_NAME}.log"

logger = init_logging(name=APP_NAME, log_level=logging.INFO, log_file=LOG_FILE)


class ResultSet:
    def __init__(self):
        self.data = defaultdict(lambda: defaultdict(dict))

    def __del__(self):
        """Print data to file"""
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2, sort_keys=True)
        logger.info(f"Output file: {OUTPUT_FILE}")


def get_instance_ids(client):
    paginator = client.get_paginator("describe_instances")
    for page in paginator.paginate():
        for item in page["Reservations"]:
            for instance in item["Instances"]:
                yield instance["InstanceOd"]


def get_launch_template_ids(client):
    paginator = client.get_paginator("describe_launch_templates")
    for page in paginator.paginate():
        for item in page["LaunchTemplates"]:
            yield item["LaunchTemplateId"]


def process(session, result):
    account_id = session.client("sts").get_caller_identity()["Account"]
    logger.info(f"Checking account {account_id}")

    client = session.client("ec2")

    # Check UserData of EC2 instances
    for instance_id in get_instance_ids(client):
        resp = client.describe_instance_attribute(Attribute="userData", InstanceId=instance_id)
        user_data = base64.b64decode(resp["UserData"]["Value"])
        result[account_id][instance_id] = user_data

    # Check UserData in Launch Configuration
    for launch_template_id in get_launch_template_ids(client):
        resp = client.describe_launch_template_versions(LaunchTemplateId=launch_template_id)
        for launch_version in resp["LaunchTemplateVersions"]:
            user_data = base64.b64decode(launch_version["LaunchTemplateData"]["UserData"])
            result[account_id][launch_template_id][launch_version["VersionNumber"]] = user_data


################################################################################
# Entry point

@click.command()
@click.option("--profile", "-p", default="default", help="AWS profile name")
def main(profile):
    result = ResultSet()

    session = Session(profile_name=profile)
    process(session, result.data)

    #for role_arn in read_role_arns_from_file(filename=DEFAULT_ROLE_ARNS_FILE):
    #    session = assume_role(role_arn=role_arn, session_name=DEFAULT_SESSION_NAME)
    #    process(session)

    logger.info(f"Log file: {LOG_FILE}")


if __name__ == "__main__": main()

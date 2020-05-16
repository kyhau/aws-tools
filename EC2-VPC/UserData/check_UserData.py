"""
Decode UserData in EC2 instances' and/or Launch Configuration Templates and output to a file
"""
import base64
from boto3.session import Session
import click
from collections import defaultdict
import json
import logging

logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger("botocore").setLevel(logging.CRITICAL)
logging.getLogger("boto3").setLevel(logging.CRITICAL)
logging.getLogger("urllib3.connectionpool").setLevel(logging.CRITICAL)


class ResultSet:
    def __init__(self, filename):
        self.data = defaultdict(lambda: defaultdict(dict))
        self.filename = filename

    def __del__(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2, sort_keys=True)
        logging.info(f"Output file: {self.filename}")


def get_instance_ids(client):
    paginator = client.get_paginator("describe_instances")
    for page in paginator.paginate():
        for item in page["Reservations"]:
            for instance in item["Instances"]:
                yield instance["InstanceId"]


def get_launch_template_ids(client):
    paginator = client.get_paginator("describe_launch_templates")
    for page in paginator.paginate():
        for item in page["LaunchTemplates"]:
            yield item["LaunchTemplateId"]


def process_ec2_instances(session, instance_id):
    """Check UserData of EC2 instances"""
    result = ResultSet("ec2_instances_userdata.json")
    client = session.client("ec2")
    instance_ids = get_instance_ids(client) if instance_id is None else [instance_id]
    for instance_id in instance_ids:
        resp = client.describe_instance_attribute(Attribute="userData", InstanceId=instance_id)
        if resp["UserData"]:
            result.data[instance_id] = base64.b64decode(resp["UserData"]["Value"])


def process_launch_templates(session, launch_template_id):
    """Check UserData in Launch Configuration"""
    result = ResultSet("launch_templates_userdata.json")
    client = session.client("ec2")
    launch_template_ids = get_launch_template_ids(client) if launch_template_id is None else [launch_template_id]
    for launch_template_id in launch_template_ids:
        resp = client.describe_launch_template_versions(LaunchTemplateId=launch_template_id)
        for launch_version in resp["LaunchTemplateVersions"]:
            result.data[launch_template_id][launch_version["VersionNumber"]] = \
                base64.b64decode(launch_version["LaunchTemplateData"]["UserData"])


@click.group(invoke_without_command=True)
@click.option("--profile", "-p", default="default", help="AWS profile name")
@click.pass_context
def cli_main(ctx, profile):
    ctx.obj["session"] =  Session(profile_name=profile)
    if ctx.invoked_subcommand is None:
        # Run both
        process_ec2_instances(ctx.obj["session"], None)
        process_launch_templates(ctx.obj["session"], None)


@cli_main.command(help="Retrieve UserData in EC2 instances")
@click.option("--instance-id", "-i", help="Instance ID. Optional.")
@click.pass_context
def instance(ctx, instance_id):
    logging.debug(f"Hello: {instance_id}, {ctx.obj}")
    process_ec2_instances(ctx.obj["session"], instance_id)


@cli_main.command(help="Retrieve UserData in Launch Templates")
@click.option("--lt-id", "-t", help="Launch Template ID. Optional.")
@click.pass_context
def launch_template(ctx, lt_id):
    logging.debug(f"launch_template: {lt_id}, {ctx.obj}")
    process_launch_templates(ctx.obj["session"], lt_id)


if __name__ == "__main__":
    cli_main(obj={})

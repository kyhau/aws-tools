import boto3
import click
import json
import logging
import sys
from arki.configs import create_ini_template, read_configs
from arki import init_logging


DEFAULT_CONFIGS = {
    "aws.profile": {"required": True},
}


def list_task_definitions(aws_profile, family_name):
    client = boto3.Session(profile_name=aws_profile).client("ecs")
    if family_name is None:
        resp = client.list_task_definitions(status="ACTIVE", sort="DESC")
    else:
        resp = client.list_task_definitions(familyPrefix=family_name, status="ACTIVE", sort="DESC")

    for arn in resp["taskDefinitionArns"]:
        print("################################################################################")
        print("Task Definition - {}".format(arn))
        resp = client.describe_task_definition(taskDefinition=arn)
        print(json.dumps(resp["taskDefinition"], sort_keys=True, indent=2))


@click.command()
@click.argument("ini_file", required=False)
@click.option("--init", "-i", is_flag=True, help="Set up new configuration")
@click.option("--family", "-f", required=False, help="Filtered by family name (ake task definition name")
def main(ini_file, init, family):
    """
    ECS

    Use --init to create a `ini_file` with the default template to start.
    """

    try:
        init_logging()

        if init:
            create_ini_template(
                ini_file=ini_file,
                module=__file__,
                config_dict=DEFAULT_CONFIGS,
                allow_overriding_default=True
            )

        else:
            profile_name=None
            if ini_file:
                settings = read_configs(ini_file=ini_file, config_dict=DEFAULT_CONFIGS)
                profile_name = settings["aws.profile"]

            list_task_definitions(aws_profile=profile_name, family_name=family)


    except Exception as e:
        logging.error(e)
        sys.exit(1)

    sys.exit(0)
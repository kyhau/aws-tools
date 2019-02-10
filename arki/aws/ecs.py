import boto3
import click
import json
import logging
from os.path import basename
from arki.configs import (
    init_wrapper,
    default_config_file_path,
)

APP_NAME = basename(__file__).split('.')[0]

# Default configuration file location
DEFAULT_CONFIG_FILE = default_config_file_path(f"{APP_NAME}.toml")

DEFAULT_CONFIGS = {
    "aws.profile": {"required": True},
}


def list_task_definitions(family_name):
    client = boto3.client("ecs")
    if family_name is None:
        resp = client.list_task_definitions(status="ACTIVE", sort="DESC")
    else:
        resp = client.list_task_definitions(familyPrefix=family_name, status="ACTIVE", sort="DESC")

    print("Task Definition ARNs:")
    print("---------------------")
    cnt = 0
    for arn in resp["taskDefinitionArns"]:
        print(f"{cnt}: {arn}")
        cnt += 1


def task_definition(arn):
    client = boto3.client("ecs")
    resp = client.describe_task_definition(taskDefinition=arn)
    print(json.dumps(resp["taskDefinition"], sort_keys=True, indent=2))


@init_wrapper
def process(*args, **kwargs):
    try:
        detail = kwargs.get("detail")
        family = kwargs.get("family")

        if detail:
            task_definition(arn=detail)
        else:
            list_task_definitions(family_name=family)

    except Exception as e:
        logging.error(e)
        return 1

    return 0


@click.command()
@click.argument("config_file", required=False, default=DEFAULT_CONFIG_FILE)
@click.option("--config_section", "-s", required=False, default=APP_NAME, help=f"E.g. {APP_NAME}.staging")
@click.option("--family", "-f", required=False, help="Filtered by family name (ake task definition name")
@click.option("--detail", "-d", required=False, help="ARN of the task definition to show more details")
def main(config_file, config_section, family, detail):
    """
    ECS
    """
    process(
        app_name=APP_NAME,
        config_file=config_file,
        default_configs=DEFAULT_CONFIGS,
        config_section=config_section,
        family=family,
        detail=detail,
    )

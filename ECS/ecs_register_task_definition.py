import boto3
import click
import json
import logging
from os.path import basename

from arki_common.configs import (
    init_wrapper,
    default_config_file_path,
)
from arki_common.utils import check_response

APP_NAME = basename(__file__).split(".")[0]

# Default configuration file location
DEFAULT_CONFIG_FILE = default_config_file_path(f"{APP_NAME}.toml")

DEFAULT_CONFIGS = {
    "aws.profile": {"required": True},
}


def get_family_name(image_url):
    """Return a string to be used as the Family Name (i.e. the Task Definition name)
    """

    # Extract the tool name and version if specified
    tool_tag = image_url.split("/")[-1]

    # E.g. updating string from sample-image:1.0.0 to sample-image-1_0_0
    family_name = tool_tag.replace(":", "-").replace(".", "_")

    # If no version specified, use `latest`
    tag_info = tool_tag.split(":")
    if len(tag_info) == 1:
        family_name = "{}-latest".format(family_name)

    logging.info("Family Name (task definition name): {}".format(family_name))
    return family_name


@init_wrapper
def process(*args, **kwargs):
    try:
        image = kwargs.get("image")
        cpu = kwargs.get("cpu")
        memory = kwargs.get("memory")
        ecs_task_role = kwargs.get("ecs_task_role")
        ecs_execution_role = kwargs.get("ecs_execution_role")
        awslogs_group = kwargs.get("awslogs_group")
        awslogs_region = kwargs.get("awslogs_region")

        family_name = get_family_name(image)

        resp = boto3.client("ecs").register_task_definition(
            family=family_name,
            taskRoleArn=ecs_task_role,
            executionRoleArn=ecs_execution_role,
            containerDefinitions=[{
                "name": family_name,
                "image": image,
                "cpu": cpu,
                "memory": memory,
                "logConfiguration": {
                    "logDriver": "awslogs",
                    "options": {
                        "awslogs-group": awslogs_group,
                        "awslogs-region": awslogs_region,
                        "awslogs-stream-prefix": family_name
                    }
                }
            }]
        )

        if not check_response(resp):
            raise Exception("Failed to register task definition")

        logging.info(json.dumps(resp, indent=2))

    except Exception as e:
        logging.error(e)
        return 1

    return 0


@click.command()
@click.argument("config_file", required=False, default=DEFAULT_CONFIG_FILE)
@click.option("--config_section", "-s", required=False, default=APP_NAME, help=f"E.g. {APP_NAME}.staging")
@click.option("--image", required=True, help="Image URI to be passed directly to the Docker daemon. E.g. 111111111111.dkr.ecr.ap-southeast-2.amazonaws.com/sample_image:latest")
@click.option("--cpu", default=2, help="The number of cpu units reserved for the container.")
@click.option("--memory", default=256, help="The hard limit (in MiB) of memory to present to the container. Default value is 256.")
@click.option("--ecs_task_role", help="ECS Task Role.")
@click.option("--ecs_execution_role", help="ECS Execution Role.")
@click.option("--awslogs_group", help="awslogs group")
@click.option("--awslogs_region", default="ap-southeast-2", help="aws-log region. Default value is ap-southeast-2.")
def register_task_definition(config_file, config_section, image, cpu, memory, ecs_task_role, ecs_execution_role, awslogs_group, awslogs_region):
    """
    Register new task definition
    """
    process(
        app_name=APP_NAME,
        config_file=config_file,
        default_configs=DEFAULT_CONFIGS,
        config_section=config_section,
        image=image,
        cpu=cpu,
        memory=memory,
        ecs_task_role=ecs_task_role,
        ecs_execution_role=ecs_execution_role,
        awslogs_group=awslogs_group,
        awslogs_region=awslogs_region,
    )

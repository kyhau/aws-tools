import boto3
import click
import json
import logging
from os.path import basename

from arki_common.aws import check_response
from arki_common.configs import (
    init_wrapper,
    default_config_file_path,
)

APP_NAME = basename(__file__).split('.')[0]

# Default configuration file location
DEFAULT_CONFIG_FILE = default_config_file_path(f"{APP_NAME}.toml")

DEFAULT_CONFIGS = {
    "aws.profile": {"required": False},
    "aws.lambda.name": {"required": True},
    "aws.lambda.alias": {"required": True},
    "aws.statemachine.arn": {"required": True},
    "aws.stepfunctions.region": {"required": True},
    "state_machine_definition_file": {"required": True},
}


def _prepare_definition(state_machine_definition_file, lambda_name, lambda_alias):
    """
    Load the state machine definition file and update with the corresponding lambda alias
    before uploading to AWS Step Functions, for deploying to different stage.
    """
    with open(state_machine_definition_file, "r") as def_json_file:
        data = json.load(def_json_file)

    # Update the `Resource` field in each "Task" block in the definition file.
    for state, attrs in data["States"].items():
        for k, v in attrs.items():
            if k == "Resource":
                ori_name = v.split(':')[-1]
                data["States"][state]["Resource"] = v.replace(ori_name, f"{lambda_name}:{lambda_alias}")

    logging.info(json.dumps(data, indent=2))
    return json.dumps(data)


def _statemachine_deploy(settings):
    """Update a state machine definition
    """
    logging.info(f"Update {settings['aws.statemachine.arn']}...")

    def_data = _prepare_definition(
        settings["state_machine_definition_file"],
        settings["aws.lambda.name"],
        settings["aws.lambda.alias"]
    )

    sfn_client = boto3.client("stepfunctions", region_name=settings["aws.stepfunctions.region"])

    resp = sfn_client._statemachine_deploy(
        stateMachineArn=settings["aws.statemachine.arn"],
        definition=def_data
    )
    return check_response(resp)


@init_wrapper
def process(*args, **kwargs):
    logging.debug("At process")
    logging.debug(kwargs)

    try:
        settings = kwargs.get("_arki_settings")
        _statemachine_deploy(settings=settings)
    except Exception as e:
        logging.error(e)
        return 1

    return 0


@click.command()
@click.argument("config_file", required=False, default=DEFAULT_CONFIG_FILE)
@click.option("--config_section", "-s", required=False, default=APP_NAME, help=f"E.g. {APP_NAME}.staging")
def lambda_deploy(config_file, config_section):

    process(
        app_name=APP_NAME,
        config_file=config_file,
        default_configs=DEFAULT_CONFIGS,
        config_section=config_section,
    )

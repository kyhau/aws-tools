import boto3
from botocore.exceptions import ClientError
import click
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
    "aws.profile": {"required": False},
    "aws.lambda.name": {"required": True},
    "aws.lambda.runtime": {"required": True},
    "aws.lambda.handler": {"required": True},
    "aws.lambda.memory": {"required": True},
    "aws.lambda.timeout": {"required": True},
    "aws.lambda.tracingconfig": {"required": False, "default": "Active"},  # Active or PassThrough
    "aws.lambda.role.arn": {"required": True},
    "aws.lambda.environment": {"multilines": True},
}


def prepare_func_configuration_args(settings, description):
    """Prepare arguments for calling update_function_configuration()
    """
    # Retrieve and prepare arguments
    func_configuration_args = {
        "Description": description,
        "FunctionName": settings["aws.lambda.name"],
        "Handler": settings["aws.lambda.handler"],
        "Role": settings["aws.lambda.role.arn"],
        "Runtime": settings["aws.lambda.runtime"],
        "MemorySize": int(settings["aws.lambda.memory"]),
        "Timeout": int(settings["aws.lambda.timeout"]),
        "TracingConfig": {"Mode": settings["aws.lambda.tracingconfig"]},
    }

    kms_key_arn = settings.get("aws.lambda.kmskey.arn")
    if kms_key_arn is not None:
        func_configuration_args["KMSKeyArn"] = kms_key_arn

    # Retrieve lambda environment variables in dict form
    env_vars = settings["aws.lambda.environment"]
    if len(env_vars) > 0:
        func_configuration_args["Environment"] = {"Variables": env_vars}

    return func_configuration_args


def _lambda_deploy(settings, zipfile, description):

    lambda_function = settings["aws.lambda.name"]
    lambda_alias = settings.get("aws.lambda.alias")
    func_configuration_args = prepare_func_configuration_args(settings, description)

    logging.info(f"Deploying (alias={lambda_alias}): {func_configuration_args}")

    with open(zipfile, mode="rb") as fh:
        byte_stream = fh.read()

    profile_name = settings.get("aws.profile")
    if profile_name is not None:
        boto3.setup_default_session(profile_name=profile_name)

    client = boto3.client("lambda", settings["aws.lambda.region"])

    resp = client.update_function_configuration(**func_configuration_args)
    check_response(resp)
    logging.info(f"Updated function config: Version={resp['Version']}, RevisionId={resp['RevisionId']}")

    resp = client.update_function_code(
        FunctionName=lambda_function,
        ZipFile=byte_stream,
        Publish=True
    )
    check_response(resp)
    version = resp["Version"]
    logging.info(f"Updated function code: Version={version}, RevisionId={resp['RevisionId']}")

    if lambda_alias is None:
        return

    alias_exists = True
    try:
        client.get_alias(FunctionName=lambda_function, Name=lambda_alias)
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceNotFoundException":
            alias_exists = False
        else:
            raise

    if alias_exists is True:
        resp = client.update_alias(
            FunctionName=lambda_function,
            Name=lambda_alias,
            FunctionVersion=version,
            Description=description,
        )
    else:
        resp = client.create_alias(
            FunctionName=lambda_function,
            Name=lambda_alias,
            FunctionVersion=version,
            Description=description,
        )
    check_response(resp)
    logging.info(f"Updated alias on Version={resp['FunctionVersion']}: AliasArn={resp['AliasArn']}")


@init_wrapper
def process(*args, **kwargs):
    logging.debug("At process")
    logging.debug(kwargs)

    try:
        if kwargs.get("is_init"):
            return 0
        
        settings = kwargs.get("_arki_settings")
        zipfile = kwargs.get("zipfile")
        description = kwargs.get("description")

        _lambda_deploy(
            settings=settings,
            zipfile=zipfile,
            description=description
        )

    except Exception as e:
        logging.error(e)
        return 1

    return 0


@click.command()
@click.argument("config_file", required=False, default=DEFAULT_CONFIG_FILE)
@click.option("--init", "-i", is_flag=True)
@click.option("--config_section", "-s", required=False, default=APP_NAME, help=f"E.g. {APP_NAME}.staging")
@click.option("--zipfile", "-z", required=False, help="Zip file of the lambda function code")
@click.option("--description", "-d", required=False, help="Description of the deployment")
def lambda_deploy(config_file, init, config_section, zipfile, description):

    process(
        app_name=APP_NAME,
        config_file=config_file,
        is_init=init,
        default_configs=DEFAULT_CONFIGS,
        config_section=config_section,
        zipfile=zipfile,
        description=description,
    )


if __name__ == "__main__": lambda_deploy()

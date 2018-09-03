import boto3
import click
import logging
import sys
from arki.aws import check_response
from arki.aws.base_helper import BaseHelper
from arki.configs import tokenize_multiline_values


DEFAULT_CONFIGS = {
    "aws.profile": {"required": False},
    "aws.lambda.name": {"required": True},
    "aws.lambda.runtime": {"required": True},
    "aws.lambda.handler": {"required": True},
    "aws.lambda.memory": {"required": True},
    "aws.lambda.timeout": {"required": True},
    "aws.lambda.role.arn": {"required": True},
    "aws.lambda.environment": {"multilines": True},
}


def retrieve_lambda_environments(settings):
    """Retrieve environment variables to be set for a stage
    """
    return tokenize_multiline_values(settings, "aws.lambda.environment")


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
    }

    kms_key_arn = settings["aws.lambda.kmskey.arn"]
    if kms_key_arn:
        func_configuration_args["KMSKeyArn"] = kms_key_arn

    # Retrieve lambda environment variables in dict form
    env_vars = retrieve_lambda_environments(settings)
    if len(env_vars) > 0:
        func_configuration_args["Environment"] = {"Variables": env_vars}
    return func_configuration_args


def _lambda_deploy(settings, zipfile, description):

    lambda_function = settings["aws.lambda.name"]
    lambda_alias = settings["aws.lambda.alias"]
    func_configuration_args = prepare_func_configuration_args(settings, description)

    logging.info(f"Deploying to {lambda_alias}: {func_configuration_args}")

    with open(zipfile, mode="rb") as fh:
        byte_stream = fh.read()

    profile_name = settings.get("aws.profile")
    if profile_name is not None:
        boto3.setup_default_session(profile_name=profile_name)

    client = boto3.client("lambda", settings["aws.lambda.region"])

    resp = client.update_function_code(
        FunctionName=lambda_function,
        ZipFile=byte_stream,
        Publish=True
    )
    check_response(resp)
    version = resp["Version"]
    logging.info(f"Updated function code: Version={version}, RevisionId={resp['RevisionId']}")

    resp = client.update_function_configuration(**func_configuration_args)
    check_response(resp)
    logging.info(f"Updated function config: Version={resp['Version']}, RevisionId={resp['RevisionId']}")

    resp = client.update_alias(
        FunctionName=lambda_function,
        Name=lambda_alias,
        FunctionVersion=version,
        Description=description,
    )
    check_response(resp)
    logging.info(f"Updated alias on Version={resp['FunctionVersion']}: AliasArn={resp['AliasArn']}")


@click.command()
@click.argument("ini_file", required=True)
@click.option("--init", "-i", is_flag=True, help="Set up new configuration")
@click.option("--zipfile", "-z", required=True, help="Zip file of the lambda function code")
@click.option("--alias", "-a", required=True, help="Alias of the deployment")
@click.option("--description", "-d", required=True, help="Description of the deployment")
def lambda_deploy(ini_file, init, zipfile, alias, description):
    """
    Use --init to create a `ini_file` with the default template to start.
    """

    try:
        helper = BaseHelper(DEFAULT_CONFIGS, ini_file, stage_section=alias)

        if init:
            helper._create_ini_template(module=__file__, allow_overriding_default=True)
        else:
            _lambda_deploy(
                settings=helper.settings,
                zipfile=zipfile,
                description=description
            )

    except Exception as e:
        logging.error(e)
        sys.exit(1)

    sys.exit(0)
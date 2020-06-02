from boto3.session import Session
from botocore.exceptions import ClientError
import click
import datetime
import json
import logging
from time import mktime

logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger("botocore").setLevel(logging.CRITICAL)
logging.getLogger("boto3").setLevel(logging.CRITICAL)
logging.getLogger("urllib3.connectionpool").setLevel(logging.CRITICAL)


class DefaultEncoder(json.JSONEncoder):
    """Encode for the json"""
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return int(mktime(obj.timetuple()))
        return json.JSONEncoder.default(self, obj)


dump_json = lambda x: json.dumps(x, cls=DefaultEncoder, sort_keys=True, indent=2)


def check_response(resp):
    """Check response and log message if needed"""
    ret = resp["ResponseMetadata"]["HTTPStatusCode"] in [200, 201, 202]
    if ret is False:
        logging.error(f"Response:\n{dump_json(resp)}")
    return ret


def read_function_configuration(config_file):
    with open(config_file, "r") as input_file:
        data = input_file.read()
        return json.loads(data)


def _lambda_deploy(session, region, function_name, config_file, zip_file, description, lambda_alias):
    client = session.client("lambda", region)

    if config_file:
        # Read configuration from config file
        function_configuration = read_function_configuration(config_file)
        function_configuration["Description"] = description
    
        if function_name != function_configuration.get("FunctionName"):
            raise ValueError(
                f"Function name not matched: arg({function_name}), "
                f"config file ({function_configuration.get('FunctionName')}))")
        logging.info(f"Deploying {function_name}:{lambda_alias}): {function_configuration}")
    
        # Update function configuration
        resp = client.update_function_configuration(**function_configuration)
        check_response(resp)
        logging.info(f"Updated function config: Version={resp['Version']}, RevisionId={resp['RevisionId']}")

    # Update function code
    with open(zip_file, mode="rb") as fh:
        byte_stream = fh.read()

    if not byte_stream:
        return

    # Update function code
    resp = client.update_function_code(
        FunctionName=function_name,
        zip_file=byte_stream,
        Publish=True
    )
    check_response(resp)
    version = resp["Version"]
    logging.info(f"Updated function code: Version={version}, RevisionId={resp['RevisionId']}")

    if lambda_alias is None:
        return

    # Update function alias
    alias_exists = True
    try:
        client.get_alias(FunctionName=function_name, Name=lambda_alias)
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceNotFoundException":
            alias_exists = False
        else:
            raise

    if alias_exists is True:
        resp = client.update_alias(
            FunctionName=function_name,
            Name=lambda_alias,
            FunctionVersion=version,
            Description=description,
        )
    else:
        resp = client.create_alias(
            FunctionName=function_name,
            Name=lambda_alias,
            FunctionVersion=version,
            Description=description,
        )
    check_response(resp)
    logging.info(f"Updated alias on Version={resp['FunctionVersion']}: AliasArn={resp['AliasArn']}")


@click.group(invoke_without_command=True, help="List name of lambda functions if no command specified")
@click.option("--profile", "-p", default="default", help="AWS profile name")
@click.option("--region", "-r", default="ap-southeast-2", help="AWS region")
@click.pass_context
def cli_main(ctx, profile, region):
    ctx.obj["session"] = Session(profile_name=profile)
    ctx.obj["region"] = region
    if ctx.invoked_subcommand is None:
        logging.info("List functions")
        client = ctx.obj["session"].client("lambda", region)
        paginator = client.get_paginator("list_functions")
        for page in paginator.paginate():
            for f in page["Functions"]:
                print(f["FunctionName"])


@cli_main.command(help="Deploy a lambda function")
@click.argument("function_name", required=True)
@click.option("--config-file", "-c", required=False, help="Json file containing lambda function configuration")
@click.option("--zip-file", "-z", required=False, help="Zip file of the lambda function code")
@click.option("--description", "-d", default="", help="Description of the deployment")
@click.option("--alias", "-a", required=False, help="Function Alias")
@click.pass_context
def deploy(ctx, function_name, zip_file, config_file, description, alias):
    logging.debug(f"deploy: {ctx.obj}")
    session, region = ctx.obj["session"], ctx.obj["region"]
    _lambda_deploy(session, region, function_name, config_file, zip_file, description, alias)


@cli_main.command(help="Export function configuration of a Lambda function")
@click.option("--function-name", "-f", help="Function name", required=True)
@click.option("--qualifier", "-q", help="Qualifier")
@click.option("--output-file", "-o", help="Output file", default="config.json")
@click.pass_context
def export_config(ctx, function_name, qualifier, output_file):
    logging.debug(f"export_function_configuration: {ctx.obj}")
    session, region = ctx.obj["session"], ctx.obj["region"]
    
    parameters = {"FunctionName": function_name}
    if qualifier:
        parameters["Qualifier"] = qualifier
    
    client = session.client("lambda", region)
    resp = client.get_function_configuration(**parameters)
    check_response(resp)
    for d in [
        "CodeSha256", "CodeSize", "FunctionArn", "ResponseMetadata", "LastModified", "LastUpdateStatus",
        "State", "Version",
    ]:
        del resp[d]
    
    with open(output_file, "w") as outfile:
        json.dump(resp, outfile, indent=2)


if __name__ == "__main__":
    cli_main(obj={})
"""
This script deploys API Gateway REST API using API Gateway Version 1.

Note: According to https://docs.aws.amazon.com/apigateway/latest/developerguide/api-ref.html
(still true on 2019-02-05)
* Amazon API Gateway Version 1 API Reference (for creating and deploying REST APIs)
* Amazon API Gateway Version 2 API Reference (for creating and deploying WebSocket/HTTP APIs)
"""
from boto3.session import Session
import click
import datetime
import io
import json
import logging
from time import mktime
import yaml

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


def get_json_data_from_file(input_file):
    """Return json object from a json or yaml file"""
    if input_file.lower().endswith(".yaml"):
        with open(input_file, "rb") as fp:
            yaml_data = fp.read()
            return io.BytesIO(json.dumps(yaml.load(yaml_data)).encode())
    else:
        with open(input_file, "r") as f:
            return json.load(f)


def check_if_stage_exists(apig_client, api_id, stage_name):
    """Check if the given stage exists, if not, create a new stage"""
    try:
        apig_client.get_stage(restApiId=api_id, stageName=stage_name)
        return True
    except apig_client.exceptions.NotFoundException as e:
        logging.debug(e)

    logging.info(f"Creating a new stage [{stage_name}]...")
    resp = apig_client.create_deployment(
        ApiId=api_id,
        Description=f"A new deployment for creating new stage: {stage_name}"
    )
    if check_response(resp) is False:
        return False

    resp = apig_client.create_stage(
        ApiId=api_id,
        StageName=stage_name,
        DeploymentId=resp["DeploymentId"]
    )
    return check_response(resp)


def create_deployment(apig_client, api_id, config):
    """Create or update a deployment stage"""
    stage_name = config["stageName"]
    logging.info(f"Creating or updating deployment stage [{stage_name}] of api gateway [{api_id}]...")
    
    resp = apig_client.create_deployment(
        restApiId=api_id,
        stageName=config["stageName"],
        stageDescription=config["description"],
        description=config["description"],
        cacheClusterEnabled=config.get("cacheClusterEnabled", False),
        cacheClusterSize=config.get("cacheClusterSize", 0.5),
        variables=config.get("variables", {}),
        canarySettings=config.get("canarySettings", {}),
        tracingEnabled=config.get("tracingEnabled", False),
    )
    return check_response(resp)


def update_stage_logging(apig_client, api_id, config):
    """
    Update logging settings of a stage.
    Note that this implemention supports only loglevel, dataTrace and metrics/enabled.
    """
    stage_name = config["stageName"]
    logging.info(f"Updating stage [{stage_name}] logging settings...")
    
    method_settings = config.get("methodSettings", {}).get("*/*", {})
    log_level = method_settings.get("loggingLevel", "OFF")
    data_trace_enabled = method_settings.get("dataTraceEnabled", False)
    metrics_enabled = method_settings.get("metricsEnabled", False)

    resp = apig_client.update_stage(
        restApiId=api_id,
        stageName=stage_name,
        patchOperations=[
            # Set Log level: OFF, ERROR, or INFO
            {"op": "replace", "path": "/*/*/logging/loglevel", "value": log_level},
            # Enable full request/response logging for all resources/methods in an API's stage
            {"op": "replace", "path": "/*/*/logging/dataTrace", "value": data_trace_enabled},
            # Enable CloudWatch metric
            {"op": "replace", "path": "/*/*/metrics/enabled", "value": metrics_enabled},
        ]
    )
    return check_response(resp)


def flush_cache(apig_client, api_id, stage_name):
    logging.info(f"Flush cache of stage [{stage_name}] of api gateway [{api_id}]...")
    resp = apig_client.flush_stage_cache(restApiId=api_id, stageName=stage_name)
    return check_response(resp)  # Return 202 if succeeded


@click.group(invoke_without_command=True, help="List REST APIs if no command specified")
@click.option("--profile", "-p", default="default", help="AWS profile name")
@click.option("--region", "-r", default="ap-southeast-2", help="AWS region")
@click.pass_context
def cli_main(ctx, profile, region):
    apig_client = Session(profile_name=profile).client("apigateway", region)
    ctx.obj["apig_client"] = apig_client
    if ctx.invoked_subcommand is None:
        logging.info("List REST APIs")
        for page in apig_client.get_paginator("get_rest_apis").paginate().result_key_iters():
            for item in page:
                print(item)


@cli_main.command(help="Reimport api swagger file to AWS api gateway")
@click.argument("api_id", required=True)
@click.option("--swagger-file", "-f", required=True, help="Swagger file in yaml (.yaml)")
@click.pass_context
def update_api(ctx, api_id, swagger_file):
    apig_client = ctx.obj["apig_client"]

    # Retrieve content of the api swagger template
    json_data = get_json_data_from_file(swagger_file)

    logging.info(f"Reimport API swagger file to api gateway {api_id}...")
    resp = apig_client.put_rest_api(restApiId=api_id, mode="overwrite", body=json_data)
    if check_response(resp) is False:
        raise Exception("Failed to reimport the api swagger file. Aborted")


@cli_main.command(help="Deploy a lambda function")
@click.argument("api_id", required=True)
@click.option("--config-file", "-c", required=False, help="Json file containing lambda function configuration")
@click.option("--description", "-d", default="", help="Description of the deployment")
@click.pass_context
def deploy(ctx, api_id, config_file, description):
    apig_client = ctx.obj["apig_client"]
    config = get_json_data_from_file(config_file)
    stage_name = config_file["stageName"]
    config["description"] = description

    logging.info(f"Create or update deployment stage [{stage_name}] of api gateway [{api_id}]...")
    
    if check_if_stage_exists(apig_client, api_id, stage_name) is False:
        raise Exception("Failed to create a new stage for deployment")
    
    if create_deployment(apig_client, api_id, config) is False:
        raise Exception("Failed to create a new deployment")

    if update_stage_logging(apig_client, api_id, config) is False:
        raise Exception("Failed to update stage logging")

    if config.get("cacheClusterEnabled", False) is True and flush_cache(apig_client, api_id, deploy) is False:
        raise Exception("Failed to flush cache.")


@cli_main.command(help="Export configuration of a REST API to restApdId-stageName-deploymentId.json")
@click.argument("api_id", required=True)
@click.pass_context
def get_stages(ctx, api_id):
    apig_client = ctx.obj["apig_client"]
    resp = apig_client.get_stages(restApiId=api_id)
    if check_response(resp) is False:
        raise Exception("Failed to get stage info")

    for d in ["ResponseMetadata"]:
        del resp[d]    # keep data needed

    for item in resp["item"]:
        logging.debug(item)
        with open(f"{api_id}-{item['stageName']}-{item['deploymentId']}.json", "w") as outfile:
            json.dump(item, outfile, cls=DefaultEncoder, sort_keys=True, indent=2)


if __name__ == "__main__":
    cli_main(obj={})

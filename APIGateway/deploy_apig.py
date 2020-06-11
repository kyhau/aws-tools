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

    logging.info(f"Creating a new stage [{stage_name}] for {api_id}...")
    resp = apig_client.create_deployment(restApiId=api_id, description=f"Initial deployment for stage: {stage_name}")
    if check_response(resp) is False:
        return False

    resp = apig_client.create_stage(restApiId=api_id, stageName=stage_name, deploymentId=resp["id"])
    return check_response(resp)


def create_deployment(apig_client, api_id, stage_name, stage_config, description):
    """Create or update a deployment stage"""
    logging.info(f"Creating or updating deployment stage [{stage_name}] of api gateway [{api_id}]...")
    
    # Pop/remove 'methodSettings` from stage_config if exists
    method_settings = stage_config.pop("methodSettings", {}).get("*/*", {})

    # Update and keep attributes required
    stage_config.update({
        "restApiId": api_id,
        "stageName": stage_name,
        "stageDescription": description,
        "description": description,
    })
    for d in ["cacheClusterStatus", "createdDate", "deploymentId", "lastUpdatedDate"]:
        if d in stage_config:
            del stage_config[d]
    if stage_config.get("canarySettings", {}).get("deploymentId") is not None:
        del stage_config["canarySettings"]["deploymentId"]
    
    resp = apig_client.create_deployment(**stage_config)
    if check_response(resp) is False:
        return False

    # Update logging settings of a stage.
    # Note that this implementation supports only loglevel, dataTrace and metrics/enabled.
    logging.info(f"Updating logging settings of stage [{stage_name}]...")
    
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
            {"op": "replace", "path": "/*/*/logging/dataTrace", "value": str(data_trace_enabled)},
            # Enable CloudWatch metric
            {"op": "replace", "path": "/*/*/metrics/enabled", "value": str(metrics_enabled)},
        ]
    )
    return check_response(resp)


def flush_cache(apig_client, api_id, stage_name):
    logging.info(f"Flush cache of stage [{stage_name}] of api gateway [{api_id}]...")
    resp = apig_client.flush_stage_cache(restApiId=api_id, stageName=stage_name)
    return check_response(resp)  # Return 202 if succeeded


@click.group(help="API Gateway deployment helper")
@click.option("--profile", "-p", default="default", show_default=True, help="AWS profile name")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS region")
@click.pass_context
def cli_main(ctx, profile, region):
    ctx.obj["apig_client"] = Session(profile_name=profile).client("apigateway", region)


@cli_main.command(help="List all REST APIs")
@click.pass_context
def ls(ctx):
    for page in ctx.obj["apig_client"].get_paginator("get_rest_apis").paginate().result_key_iters():
        for item in page:
            print(item)


@cli_main.command(help="Deploy a REST API to the specified stage")
@click.argument("api_id", required=True)
@click.option("--description", "-d", default="", help="Description of the new deployment")
@click.option("--stage-config-file", "-f", required=True, help="Json file containing same info from get_stage")
@click.option("--stage-name", "-n", required=True, help="Stage name, no space")
@click.pass_context
def deploy(ctx, api_id, description, stage_config_file, stage_name):
    apig_client = ctx.obj["apig_client"]
    stage_config = get_json_data_from_file(stage_config_file)
    
    if check_if_stage_exists(apig_client, api_id, stage_name) is False:
        raise Exception("Failed to create a new stage for deployment")

    if create_deployment(apig_client, api_id, stage_name, stage_config, description) is False:
        raise Exception("Failed to create a new deployment")

    if stage_config.get("cacheClusterEnabled", False) is True and flush_cache(apig_client, api_id, deploy) is False:
        raise Exception("Failed to flush cache.")


@cli_main.command(help="Export stage info (get_stage) of a REST API to restApiId-stageName-deploymentId.json")
@click.argument("api_id", required=True)
@click.pass_context
def get_stages(ctx, api_id):
    apig_client = ctx.obj["apig_client"]
    resp = apig_client.get_stages(restApiId=api_id)
    if check_response(resp) is False:
        raise Exception("Failed to get stage configuration")

    for item in resp["item"]:
        logging.debug(item)
        with open(f"{api_id}-{item['stageName']}-{item['deploymentId']}.json", "w") as outfile:
            json.dump(item, outfile, cls=DefaultEncoder, sort_keys=True, indent=2)


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


if __name__ == "__main__":
    cli_main(obj={})

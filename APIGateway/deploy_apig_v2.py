"""
This script deploys WebSocket/HTTP API Gateway using API Gateway Version 2.

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
        apig_client.get_stage(ApiId=api_id, StageName=stage_name)
        return True
    except apig_client.exceptions.NotFoundException as e:
        logging.debug(e)

    logging.info(f"Creating a new stage [{stage_name}] for {api_id}...")
    resp = apig_client.create_deployment(ApiId=api_id, Description=f"Initial deployment for stage: {stage_name}")
    if check_response(resp) is False:
        return False

    resp = apig_client.create_stage(ApiId=api_id, StageName=stage_name, DeploymentId=resp["DeploymentId"])
    return check_response(resp)


def create_deployment(apig_client, api_id, stage_name, stage_config, description):
    """Create or update a deployment stage"""
    logging.info(f"Creating or updating deployment stage [{stage_name}] of api gateway [{api_id}]...")

    resp = apig_client.create_deployment(ApiId=api_id, Description=description, StageName=stage_name)
    if check_response(resp) is False:
        return False

    deployment_id = resp["DeploymentId"]
    logging.info(f"Updating logging settings of stage [{stage_name}] ({deployment_id})...")

    # Update and keep attributes required
    stage_config.update({
        "ApiId": api_id,
        "DeploymentId": deployment_id,
        "Description": description,
        "StageName": stage_name,
    })
    for d in ["CreatedDate", "LastUpdatedDate", "Tags"]:
        if d in stage_config:
            del stage_config[d]
    
    resp = apig_client.update_stage(**stage_config)
    return check_response(resp)


@click.group(invoke_without_command=True, help="List WebSocket/HTTP APIs if no command specified")
@click.option("--profile", "-p", default="default", help="AWS profile name")
@click.option("--region", "-r", default="ap-southeast-2", help="AWS region")
@click.pass_context
def cli_main(ctx, profile, region):
    apig_client = Session(profile_name=profile).client("apigatewayv2", region)
    ctx.obj["apig_client"] = apig_client
    if ctx.invoked_subcommand is None:
        logging.info("List WebSocket/HTTP APIs")
        for page in apig_client.get_paginator("get_apis").paginate().result_key_iters():
            for item in page:
                print(item)


@cli_main.command(help="Deploy a WebSocket/HTTP API to the specified stage")
@click.argument("api_id", required=True)
@click.option("--description", "-d", default="", help="Description of the new deployment")
@click.option("--stage-config-file", "-f", required=True, help="Json file containing same infor from get_stage")
@click.option("--stage-name", "-n", required=True, help="Stage name, no space")
@click.pass_context
def deploy(ctx, api_id, description, stage_config_file, stage_name):
    apig_client = ctx.obj["apig_client"]
    stage_config = get_json_data_from_file(stage_config_file)
    
    if check_if_stage_exists(apig_client, api_id, stage_name) is False:
        raise Exception("Failed to create a new stage for deployment")
    
    if create_deployment(apig_client, api_id, stage_name, stage_config, description) is False:
        raise Exception("Failed to create a new deployment")
    
    # WebSocket does not have caching related settings (e.g. "cache cluster enabled")


@cli_main.command(help="Export stage info (get_stage) of a WebSocket/HTTP API to ApiId-StageName-DeploymentId.json")
@click.argument("api_id", required=True)
@click.pass_context
def get_stages(ctx, api_id):
    apig_client = ctx.obj["apig_client"]
    for page in apig_client.get_paginator("get_stages").paginate(ApiId=api_id).result_key_iters():
        for item in page:
            logging.debug(item)
            with open(f"{api_id}-{item['StageName']}-{item['DeploymentId']}.json", "w") as outfile:
                json.dump(item, outfile, cls=DefaultEncoder, sort_keys=True, indent=2)


if __name__ == "__main__":
    cli_main(obj={})

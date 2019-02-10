import boto3
import click
import io
import json
import logging
from os.path import basename
import yaml
from arki.aws import check_response
from arki.configs import (
    init_wrapper,
    default_config_file_path,
)

APP_NAME = basename(__file__).split('.')[0]

# Default configuration file location
DEFAULT_CONFIG_FILE = default_config_file_path(f"{APP_NAME}.toml")

DEFAULT_CONFIGS = {
    "aws.profile": {"required": True},
    "aws.apigateway.restapiid": {"required": True},
    "aws.apigateway.swaggeryaml": {"required": True},
    "aws.apigateway.cacheclusterenabled": {"default": True},
    "aws.apigateway.cacheclustersize": {"default": 0},
    "aws.apigateway.datatraceenabled": {"default": True},
    "aws.apigateway.logginglevel": {"default": "ERROR"},
    "aws.apigateway.metricsenabled": {"default": True},
    "aws.apigateway.stagevariables": {"multilines": True},
}


def put_rest_api(apig_client, rest_api_id, swagger_file_yaml):
    """Reimport api swagger file to AWS api gateway
    """
    
    # Retrieve content of the api swagger template
    with open(swagger_file_yaml, "rb") as fp:
        yaml_data = fp.read()
        json_data = io.BytesIO(json.dumps(yaml.load(yaml_data)).encode())

    logging.info(f"Reimport API swagger file to api gateway [{rest_api_id}]...")
    resp = apig_client.put_rest_api(
        restApiId=rest_api_id,
        mode="overwrite",
        body=json_data
    )
    return check_response(resp)


def flush_cache(apig_client, rest_api_id, stage_name):
    logging.info(f"Flush cache of stage [{stage_name}] of api gateway [{rest_api_id}]...")

    resp = apig_client.flush_stage_cache(
        restApiId=rest_api_id,
        stageName=stage_name
    )
    # Return 202 if succeeded
    return check_response(resp)


def create_deployment(apig_client, rest_api_id, stage_name, stage_variables_dict, cache_cluster_enabled=False, cache_cluster_size=0):
    """Create or update a deployment stage
    """
    logging.info(f"Create or update deployment stage [{stage_name}] of api gateway [{rest_api_id}]...")

    resp = apig_client.create_deployment(
        restApiId=rest_api_id,
        stageName=stage_name,
        stageDescription=stage_name,
        description=stage_name,
        cacheClusterEnabled=cache_cluster_enabled,
        cacheClusterSize=cache_cluster_size,
        variables=stage_variables_dict
    )
    return check_response(resp)


def update_stage_logging(apig_client, rest_api_id, stage_name, data_trace_enabled, log_level, metrics_enabled):
    """Update logging settings of a stage
    """
    logging.info(f"Update stage [{stage_name}] logging settings...")

    resp = apig_client.update_stage(
        restApiId=rest_api_id,
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


@init_wrapper
def process(*args, **kwargs):
    try:
        settings = kwargs.get("_arki_settings")
        deploy = kwargs.get("deploy")

        apig_client = boto3.client("apigateway")

        rest_api_id = settings["aws.apigateway.restapiid"]
        swagger_file_yaml = settings["aws.apigateway.swaggeryaml"]
        cache_cluster_enabled = settings.get("aws.apigateway.cacheclusterenabled", False)
        stage_variables_dict = settings.get("aws.apigateway.stagevariables", {})
        cache_cluster_size = settings.get("aws.apigateway.cacheclustersize", 0)

        log_level = settings["aws.apigateway.logginglevel"]
        data_trace_enabled = settings["aws.apigateway.datatraceenabled"]
        metrics_enabled = settings["aws.apigateway.metricsenabled"]

        # Put the rest api to AWS
        if put_rest_api(apig_client, rest_api_id, swagger_file_yaml) is False:
            raise Exception("Failed to reimport the api swagger file. Aborted")

        if deploy:
            # Create a deployment for the given stage
            ret = create_deployment(
                apig_client=apig_client,
                rest_api_id=rest_api_id,
                stage_name=deploy,
                stage_variables_dict=stage_variables_dict,
                cache_cluster_enabled=cache_cluster_enabled,
                cache_cluster_size=cache_cluster_size
            )
            if ret:
                ret = update_stage_logging(
                    apig_client=apig_client,
                    rest_api_id=rest_api_id,
                    stage_name=deploy,
                    data_trace_enabled=data_trace_enabled,
                    log_level=log_level,
                    metrics_enabled=metrics_enabled
                )
            if ret and cache_cluster_enabled:
                ret = flush_cache(apig_client, rest_api_id, deploy)
                if ret is False:
                    raise Exception("Failed to flush cache.")
            else:
                raise Exception("Failed to create deployment stage. Aborted")

    except Exception as e:
        logging.error(e)
        return 1

    return 0


@click.command()
@click.argument("config_file", required=False, default=DEFAULT_CONFIG_FILE)
@click.option("--config_section", "-s", required=False, default=APP_NAME, help=f"E.g. {APP_NAME}.staging")
@click.option("--deploy", "-d", required=False, help="Deploy the current rest api to a stage. Choices: [test, staging, v1]")
def main(config_file, config_section, deploy):
    """
    Reimport the API Swagger template to AWS.

    If `deploy` is specified, the program will instead deploy the current REST
    api to the specified stage.
    """
    process(
        app_name=APP_NAME,
        config_file=config_file,
        default_configs=DEFAULT_CONFIGS,
        config_section=config_section,
        deployt=deploy,
    )

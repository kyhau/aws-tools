import boto3
import click
import io
import json
import logging
import sys
import yaml

from . import check_response
from arki.configs import create_ini_template, read_configs
from arki import init_logging


DEFAULT_CONFIGS = {
    "aws.profile": {"required": True},
    "aws.apigateway.restapiid": {"required": True},
    "aws.apigateway.swaggeryaml": {"required": True},
    "aws.apigateway.cacheclusterenabled": {"default": True},
    "aws.apigateway.cacheclustersize": {"default": 0},
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


@click.command()
@click.argument("ini_file", required=True)
@click.option("--init", "-i", is_flag=True, help="Set up new configuration")
@click.option("--deploy", "-d", required=False, help="Deploy the current rest api to a stage. Choices: [dev, staging, v1]")
def main(ini_file, init, deploy):
    """
    Reimport the API Swagger template to AWS.

    If `deploy` is specified, the program will instead deploy the current REST
    api to the specified stage.
    """

    init_logging()

    if init:
        return create_ini_template(
            ini_file=ini_file,
            module=__file__,
            config_dict=DEFAULT_CONFIGS,
            allow_overriding_default=True
        )

    ret_code = 0

    try:
        settings = read_configs(
            ini_file=ini_file,
            config_dict=DEFAULT_CONFIGS,
            section_list=[deploy] if deploy else None
        )

        apig_client = boto3.Session(profile_name=settings["aws.profile"]).client("apigateway")

        rest_api_id = settings["aws.apigateway.restapiid"]
        swagger_file_yaml = settings["aws.apigateway.swaggeryaml"]
        cache_cluster_enabled = settings.get("aws.apigateway.cacheclusterenabled", False)
        stage_variables_dict = settings.get("aws.apigateway.stagevariables", {})
        cache_cluster_size = settings.get("aws.apigateway.cacheclustersize", 0)

        # Put the rest api to AWS
        if put_rest_api(apig_client, rest_api_id, swagger_file_yaml) is False:
            logging.error("Failed to reimport the api swagger file. Aborted")
            return 1

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
            if ret and cache_cluster_enabled:
                ret = flush_cache(apig_client, rest_api_id, deploy)
                if ret is False:
                    logging.error("Failed to flush cache.")
            else:
                logging.error("Failed to create deployment stage. Aborted")
                return 1

        return 0


    except Exception as e:
        logging.error(e)
        ret_code = 1

    sys.exit(ret_code)
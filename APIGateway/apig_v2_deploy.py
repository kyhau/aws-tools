"""
This script deploys API Gateway WebSocket API using API Gateway Version 2.

Note: According to https://docs.aws.amazon.com/apigateway/latest/developerguide/api-ref.html
(still true on 2019-02-05)
* Amazon API Gateway Version 1 API Reference (for creating and deploying HTTP APIs)
* Amazon API Gateway Version 2 API Reference (for creating and deploying WebSocket APIs)
"""
import boto3
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
    "aws.profile": {"required": True},
    "aws.apigateway.apiid": {"required": True},
    "aws.apigateway.datatraceenabled": {"default": True},
    "aws.apigateway.logginglevel": {"default": "ERROR"},
    "aws.apigateway.metricsenabled": {"default": True},
    "aws.apigateway.stagevariables": {"multilines": True},
    "aws.apigateway.integrations.lambdas": {"multilines": True},
}


def check_if_stage_exists(apig_client, apiid, stage_name):
    """Check if the given stage exists, if not, create a new stage
    """
    try:
        apig_client.get_stage(ApiId=apiid, StageName=stage_name)
        return True

    except apig_client.exceptions.NotFoundException as e:
        logging.info(e)

    logging.info(f"Create stage: {stage_name}")
    resp = apig_client.create_deployment(
        ApiId=apiid,
        Description=f"Preparing a deployment for creating new stage: {stage_name}"
    )
    ret = check_response(resp)

    if ret:
        resp = apig_client.create_stage(
            ApiId=apiid,
            StageName=stage_name,
            DeploymentId=resp["DeploymentId"]
        )
        ret = check_response(resp)
    return ret


def create_deployment(
        apig_client, apiid, stage_name, description, stage_variables_dict,
        data_trace_enabled, log_level, metrics_enabled
):
    """Create or update a deployment stage
    """
    logging.info(f'Create or update deployment stage [{stage_name}] of api gateway [apiid] ...')

    if check_if_stage_exists(apig_client, apiid, stage_name) is False:
        return False

    resp = apig_client.create_deployment(
        ApiId=apiid,
        Description=description,
        StageName=stage_name
    )
    if check_response(resp) is False:
        return False

    deployment_id = resp["DeploymentId"]
    logging.info(f"deployment_id: {deployment_id}")

    logging.info(f"Update stage [{stage_name}] logging settings ...")
    resp = apig_client.update_stage(
        ApiId=apiid,
        DefaultRouteSettings={
            "DataTraceEnabled": data_trace_enabled,
            "DetailedMetricsEnabled": metrics_enabled,
            "LoggingLevel": log_level,
        },
        DeploymentId=deployment_id,
        Description=description,
        StageName=stage_name,
        StageVariables=stage_variables_dict,
    )

    # WebSocket does not have caching related settings (e.g. "cache cluster enabled")

    return check_response(resp)


@init_wrapper
def process(*args, **kwargs):
    try:
        if kwargs.get("is_init"):
            return 0
        
        settings = kwargs.get("_arki_settings")
        deploy = kwargs.get("deploy")
        description = kwargs.get("description")

        apig_client = boto3.client("apigatewayv2")

        apiid = settings["aws.apigateway.apiid"]
        stage_variables_dict = settings.get("aws.apigateway.stagevariables", {})

        log_level = settings["aws.apigateway.logginglevel"]
        data_trace_enabled = settings["aws.apigateway.datatraceenabled"]
        metrics_enabled = settings["aws.apigateway.metricsenabled"]

        # Currently AWS only supports importing swagger file for REST API, not WebSocket API.

        if deploy:
            # Create a deployment for the given stage
            ret = create_deployment(
                apig_client=apig_client,
                apiid=apiid,
                stage_name=deploy,
                stage_variables_dict=stage_variables_dict,
                description=description,
                data_trace_enabled=data_trace_enabled,
                log_level=log_level,
                metrics_enabled=metrics_enabled
            )
            if ret is False:
                raise Exception("Failed to create deployment stage. Aborted")

    except Exception as e:
        logging.error(e)
        return 1

    return 0


@click.command()
@click.argument("config_file", required=False)
@click.option("--init", "-i", is_flag=True)
@click.option("--config_section", "-s", required=False, default=APP_NAME, help=f"E.g. {APP_NAME}.staging")
@click.option("--deploy", "-d", required=False, help="Deploy the current rest api to a stage. Choices: [test, staging, v1]")
@click.option("--description", required=False, help="Deployment description")
def main(config_file, init, config_section, deploy, description):
    process(
        app_name=APP_NAME,
        is_init=init,
        config_file=config_file,
        default_configs=DEFAULT_CONFIGS,
        config_section=config_section,
        deploy=deploy,
        description=description
    )


if __name__ == "__main__":
    main()

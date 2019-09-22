import boto3
import click
import json
import logging
from os.path import basename
import re

from arki_common.configs import (
    init_wrapper,
    default_config_file_path,
)
from arki_common.utils import (
    check_response,
    DefaultEncoder,
    HTTPS_OK_CODES,
)

APP_NAME = basename(__file__).split(".")[0]

# Default configuration file location
DEFAULT_CONFIG_FILE = default_config_file_path(f"{APP_NAME}.toml")

DEFAULT_CONFIGS = {
    "aws.profile": {"required": True},
    "aws.lambda.name": {"required": True},
    "aws.lambda.aliases": {"multilines": True},
    "aws.apigateway.restapiid": {"required": True},
    "aws.apigateway.accountid": {"required": True},
    "aws.apigateway.region": {"required": True, "default": "ap-southeast-2"},
}


def add_lambda_permissions(lambda_function, lambda_aliases, resource_arns):
    """
    Add lambda permission for all api gateway resources (routes) to access the lambda function

    :param lambda_function: Name of the Lambda function
    :param lambda_aliases: List of Lambda aliases
    :param apig_resource_arns: List of ARNs of AWS resources
    """
    lambda_client = boto3.client("lambda")

    for lambda_alias in lambda_aliases:
        for (arn, statement_id) in resource_arns:
            logging.info(
                f"Add lambda permission to {arn} (statement_id={statement_id}) for accessing "
                f"{lambda_function}:{lambda_alias}"
            )
            try:
                resp = lambda_client.add_permission(
                    FunctionName=lambda_function,
                    StatementId=statement_id,
                    Action="lambda:InvokeFunction",
                    Principal="apigateway.amazonaws.com",
                    SourceArn=arn,
                    Qualifier=lambda_alias
                )
                check_response(resp)
            except Exception as e:
                logging.warning(str(e))


def get_apig_resource_arns(apig_id, apig_region, apig_account_id):
    """
    Return list of (resource-path-arns, statement-id)

    :param apig_id: API Gateway ID (aka restapiid)
    :param apig_region: API Gateway region
    :param apig_account_id: AWS account ID of the API Gateway
    :return: list of (resource-path-arns, statement-id)
    """

    apig_client = boto3.client("apigateway")

    resp = apig_client.get_resources(restApiId=apig_id, limit=50)
    if check_response(resp) is False:
        raise Exception("Failed to retrieve api gateway resource paths. Aborted")

    apig_base_url = f"arn:aws:execute-api:{apig_region}:{apig_account_id}:{apig_id}/*/"

    arn_list = []
    for item in resp["items"]:
        if "resourceMethods" in item.keys():
            for method in item["resourceMethods"].keys():
                actual_path = method + re.sub("\{.*?\}", "*", item["path"])
                statement_id = re.sub("[\/\*]", "", actual_path).lower()
                arn_list.append(("{}{}".format(apig_base_url, actual_path), statement_id))

    return arn_list


def get_apig_route_arns(apig_id, apig_region, apig_account_id):
    """Return list of (route-arns, statement-id)

    :param apig_id: API Gateway ID (aka apiid)
    :param apig_region: API Gateway region
    :param apig_account_id: AWS account ID of the API Gateway
    """
    apig_client = boto3.client("apigatewayv2")

    resp = apig_client.get_routes(ApiId=apig_id)
    ret = resp["ResponseMetadata"]["HTTPStatusCode"] in HTTPS_OK_CODES
    if ret is False:
        logging.info(f"Response:\n{json.dumps(resp, cls=DefaultEncoder, sort_keys=True, indent=2)}")
        return None

    apig_base_url = f"arn:aws:execute-api:{apig_region}:{apig_account_id}:{apig_id}/*/"

    arn_list = []
    for item in resp["Items"]:
        if "RouteKey" in item.keys():
            # arn:aws:execute-api:region:account-id:api-id/stage-name/route-key
            statement_id = re.sub("[\/\$]", "", item["RouteKey"]).lower()
            arn_list.append((f"{apig_base_url}{item['RouteKey']}", statement_id))

    return arn_list


@init_wrapper
def process(*args, **kwargs):
    try:
        settings = kwargs.get("_arki_settings")

        if settings.get("aws.apigateway.restapiid") is not None:
            arn_list = get_apig_resource_arns(
                apig_id=settings["aws.apigateway.restapiid"],
                apig_region=settings["aws.apigateway.region"],
                apig_account_id=settings["aws.apigateway.accountid"]
            )
        else:
            arn_list = get_apig_route_arns(
                apig_id=settings["aws.apigateway.restapiid"],
                apig_region=settings["aws.apigateway.region"],
                apig_account_id=settings["aws.apigateway.accountid"]
            )

        add_lambda_permissions(
            lambda_function=settings["aws.lambda.name"],
            lambda_aliases=settings.get("aws.lambda.aliases", [None]),
            resource_arns=arn_list
        )
    except Exception as e:
        logging.error(e)
        return 1

    return 0


@click.command()
@click.argument("config_file", required=False, default=DEFAULT_CONFIG_FILE)
@click.option("--config_section", "-s", required=False, default=APP_NAME, help=f"E.g. {APP_NAME}.staging")
def lambda_permissions_to_apig(config_file, config_section):
    """
    Add Lambda Permissions to a API Gateway.
    """
    process(
        app_name=APP_NAME,
        config_file=config_file,
        default_configs=DEFAULT_CONFIGS,
        config_section=config_section,
    )

import boto3
import click
import logging
import re
import sys
from arki.aws import check_response
from arki.aws.base_helper import BaseHelper


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
            logging.info(f"Add lambda permission to {arn} (statement_id={statement_id}) for accessing alias {lambda_alias}")
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

    apig_base_url = "arn:aws:execute-api:{}:{}:{}/*/".format(apig_region, apig_account_id, apig_id)

    arn_list = []
    for item in resp["items"]:
        if "resourceMethods" in item.keys():
            for method in item["resourceMethods"].keys():
                actual_path = method + re.sub("\{.*?\}", "*", item["path"])
                statement_id = re.sub("[\/\*]", "", actual_path).lower()
                arn_list.append(("{}{}".format(apig_base_url, actual_path), statement_id))

    return arn_list


@click.command()
@click.argument("ini_file", required=True)
@click.option("--init", "-i", is_flag=True, help="Set up new configuration")
def lambda_permissions_to_apig(ini_file, init):
    """
    Add Lambda Permissions to a API Gateway.

    Use --init to create a `ini_file` with the default template to start.
    """

    try:
        helper = BaseHelper(DEFAULT_CONFIGS, ini_file)

        if init:
            helper._create_ini_template(module=__file__, allow_overriding_default=False)
        else:
            arn_list = get_apig_resource_arns(
                apig_id=helper.settings["aws.apigateway.restapiid"],
                apig_region=helper.settings["aws.apigateway.region"],
                apig_account_id=helper.settings["aws.apigateway.accountid"]
            )

            add_lambda_permissions(
                lambda_function=helper.settings["aws.lambda.name"],
                lambda_aliases=helper.settings.get("aws.lambda.aliases", [None]),
                resource_arns=arn_list
            )

    except Exception as e:
        logging.error(e)
        sys.exit(1)

    sys.exit(0)
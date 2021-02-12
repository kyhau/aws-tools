"""
This scripts add lambda permission for all api gateway resources (or routes if apigv2) to access the lambda function.
"""
from boto3.session import Session
import click
import datetime
import json
import logging
import re
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


def add_lambda_permissions(session, lambda_function, lambda_alias, lambda_region, resource_arns):
    """
    Add lambda permission for all api gateway resources (or routes if apigv2) to access the lambda function
    :param lambda_function: Name of the Lambda function
    :param lambda_alias:  The version or alias to add permissions to a published version of the function.
    :param lambda_region: Region of the Lambda function
    :param apig_resource_arns: List of ARNs of AWS resources
    """
    lambda_client = session.client("lambda", lambda_region)
    
    params = {
        "FunctionName": lambda_function,
        "Action": "lambda:InvokeFunction",
        "Principal": "apigateway.amazonaws.com",
    }
    if lambda_alias:
        params["Qualifier"] = lambda_alias

    for (arn, statement_id) in resource_arns:
        logging.info(
            f"Add lambda permission to {arn} (statement_id={statement_id}) for accessing "
            f"{lambda_function}:{lambda_alias}"
        )
        params.update({
            "SourceArn": arn,
            "StatementId": statement_id,
        })
        try:
            resp = lambda_client.add_permission(**params)
            check_response(resp)
        except Exception as e:
            logging.warning(str(e))


def get_apig_resource_arns(session, apig_id, apig_region, apig_account_id):
    """
    Return list of (resource-path-arns, statement-id)
    :param apig_id: API Gateway ID (aka restapiid)
    :param apig_region: API Gateway region
    :param apig_account_id: AWS account ID of the API Gateway
    :return: list of (resource-path-arns, statement-id)
    """
    resp = session.client("apigateway", apig_region).get_resources(restApiId=apig_id, limit=50)
    if check_response(resp) is False:
        raise Exception("Failed to retrieve api gateway resource paths. Aborted")

    apig_base_url = f"arn:aws:execute-api:{apig_region}:{apig_account_id}:{apig_id}/*/"

    arn_list = []
    for item in resp["items"]:
        if "resourceMethods" in item.keys():
            for method in item["resourceMethods"].keys():
                actual_path = method + re.sub("\{.*?\}", "*", item["path"])
                statement_id = re.sub("[\/\*]", "", actual_path).lower()
                arn_list.append((f"{apig_base_url}{actual_path}", statement_id))

    return arn_list


def get_apig_route_arns(session, apig_id, apig_region, apig_account_id):
    """
    Return list of (route-arns, statement-id)
    :param apig_id: API Gateway ID (aka apiid)
    :param apig_region: API Gateway region
    :param apig_account_id: AWS account ID of the API Gateway
    """
    resp = session.client("apigatewayv2", apig_region).get_routes(ApiId=apig_id)
    if check_response(resp) is False:
        raise Exception("Failed to retrieve api gateway routes. Aborted")

    apig_base_url = f"arn:aws:execute-api:{apig_region}:{apig_account_id}:{apig_id}/*/"

    arn_list = []
    for item in resp["Items"]:
        if "RouteKey" in item.keys():
            # arn:aws:execute-api:region:account-id:api-id/stage-name/route-key
            statement_id = re.sub("[\/\$]", "", item["RouteKey"]).lower()
            arn_list.append((f"{apig_base_url}{item['RouteKey']}", statement_id))

    return arn_list


@click.group(help="Add Lambda Permission for a REST/WebSocket/HTTP API Gateway")
@click.argument("lambda_name", required=True)
@click.option("--apig-id", required=True, help="API Gateway ID")
@click.option("--apig-region", default="ap-southeast-2", show_default=True, help="API Gateway region")
@click.option("--lambda-alias", help="The version or alias to add permissions to a published version of the function")
@click.option("--lambda-region", default="ap-southeast-2", show_default=True, help="Lambda region")
@click.option("--profile", "-p", default="default", help="AWS profile name")
@click.pass_context
def cli_main(ctx, lambda_name, apig_id, apig_region, lambda_alias, lambda_region, profile):
    session = Session(profile_name=profile)
    account_id = session.client("sts").get_caller_identity()["Account"]
    ctx.obj = {
        "apig": {
            "session": session,
            "apig_id": apig_id,
            "apig_region": apig_region,
            "apig_account_id": account_id,
        },
        "lambda": {
            "session": session,
            "lambda_alias": lambda_alias,
            "lambda_name": lambda_name,
            "lambda_region": lambda_region,
        }
    }


@cli_main.command(help="Add lambda permission for all resources of a REST API to access the lambda function")
@click.pass_context
def apigateway(ctx):
    arn_list = get_apig_resource_arns(**ctx.obj["apig"])
    add_lambda_permissions(resource_arns=arn_list, **ctx.obk["lambda"])


@cli_main.command(help="Add lambda permission for all routes of a WebSocket/HTTP API to access the lambda function")
@click.pass_context
def apigatewayv2(ctx):
    arn_list = get_apig_route_arns(**ctx.obj["apig"])
    add_lambda_permissions(resource_arns=arn_list, **ctx.obk["lambda"])


if __name__ == "__main__":
    cli_main(obj={})

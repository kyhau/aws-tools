"""
1. List all REST/HTTP/WEBSOCKET APIGWs, or
1. Lookup details of a APIGW by its ID
"""
import json
import logging

import click
from helper.aws import AwsApiHelper

logging.getLogger().setLevel(logging.INFO)


class Helper(AwsApiHelper):
    def __init__(self, detailed):
        super().__init__()
        self._detailed = detailed

    def process_request(self, session, account_id, region, kwargs):
        api_id = kwargs.get("id")

        client = session.client("apigateway", region_name=region)
        for item in self.paginate(client, "get_rest_apis", kwargs):
            if api_id:
                if api_id == item.get("id"):
                    print(json.dumps(item, indent=2, default=str))
                    return True
            else:
                if self._detailed:
                    print(json.dumps(item, indent=2, default=str))
                else:
                    config = item.get("endpointConfiguration", {})
                    types = "|".join(config.get("types", []))
                    endpoints = "|".join(config.get("vpcEndpointIds", ["NoVpcEndpoint"]))
                    print(", ".join([account_id, item.get("id"), f"REST {types}", item.get("name"), endpoints]))

        client = session.client("apigatewayv2", region_name=region)
        for page in client.get_paginator("get_apis").paginate().result_key_iters():
            for item in page:
                if api_id:
                    if api_id == item.get("ApiId"):
                        print(json.dumps(item, indent=2, default=str))
                        return True
                else:
                    if self._detailed:
                        print(json.dumps(item, indent=2, default=str))
                    else:
                        print(", ".join([account_id, item.get("ApiId"), item.get("ProtocolType"), item.get("Name"), item.get("ApiEndpoint")]))


@click.command()
@click.option("--detailed", "-d", is_flag=True, default=False, help="Show details instead of just layer ARNs.")
@click.option("--id", "-i", help="API gateway ID. List all APIs if not specified.")
@click.option("--profile", "-p", help="AWS profile name. Use profiles in ~/.aws if not specified.")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS Region. Use 'all' for all regions.")
def main(detailed, id, profile, region):
    kwargs = {"id": id} if id else {}
    Helper(detailed).start(profile, region, "apigateway", kwargs)


if __name__ == "__main__":
    main()

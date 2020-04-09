"""
API:
1. Create short URL: HTTP GET ?targetUrl=
2. Read   short URL: HTTP GET /<id>

API Gateway, Lambda, DynamoDB (+ monitoring and traffic generator)
"""
from aws_cdk.core import Construct, Duration, Stack, CfnOutput, Fn
from aws_cdk import aws_apigateway, aws_dynamodb, aws_ec2, aws_lambda
from cdk_watchful import Watchful
from os import environ

from .traffico import Traffico


VPC_ID = environ.get("VPC_ID")
ALERT_EMAIL = environ.get("ALERT_EMAIL")


# Main application stack
class UrlShortenerStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here
        table = aws_dynamodb.Table(
            self, "ShortCodeMappingTable",
            partition_key=aws_dynamodb.Attribute(name="id", type=aws_dynamodb.AttributeType.STRING))
        
        function = aws_lambda.Function(
            self, "UrlShortenerFunction",
            code=aws_lambda.Code.asset("./lambda"),
            handler="handler.main",
            timeout=Duration.minutes(5),
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            tracing=aws_lambda.Tracing.ACTIVE,
        )
        
        table.grant_read_write_data(function)
        
        function.add_environment("TABLE_NAME", table.table_name)
        
        api = aws_apigateway.LambdaRestApi(self, "UrlShortenerApi", handler=function)
        
        wf = Watchful(self, "watchful", alarm_email=ALERT_EMAIL)
        wf.watch_scope(self)
        
        CfnOutput(self, "UrlShortenerApiUrl", value=api.url, export_name="UrlShortenerApiUrl")


# Separate stack that includes the traffic generator
class TrafficStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        Traffico(
            self, "TrafficGenerator",
            vpc=aws_ec2.Vpc.from_lookup(self, "vpc", vpc_id=VPC_ID),
            url=Fn.import_value("UrlShortenerApiUrl"),
            tps=10)

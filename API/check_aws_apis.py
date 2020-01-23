"""
A script to check some AWS APIs current status.
"""
from boto3.session import Session
from botocore.exceptions import ClientError
import click
import logging

# Update the root logger to get messages at DEBUG and above
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("botocore").setLevel(logging.CRITICAL)
logging.getLogger("boto3").setLevel(logging.CRITICAL)
logging.getLogger("urllib3").setLevel(logging.CRITICAL)

API_TESTS = {
    "acm": ("list_certificates", {"MaxItems": 1}),
    "apigateway": ("get_rest_apis", {"limit": 1}),
    "apigatewayv2": ("get_apis", {"MaxResults": "1"}),
    "athena": ("list_work_groups", {}),
    
    "autoscaling": ("describe_auto_scaling_instances", {"MaxRecords": 1}),
    "backup": ("list_backup_jobs", {"MaxResults": 1}),
    "cloudformation": ("list_stacks", {}),
    "cloudfront": ("list_distributions", {"MaxItems": "1"}),
    "cloudtrail": ("describe_trails", {}),
    "cloudwatch": ("describe_alarms", {"MaxRecords": 1}),
    "codebuild": ("list_projects", {}),
    "codecommit": ("list_repositories", {}),
    "codedeploy": ("list_applications", {}),
    "codepipeline": ("list_pipelines", {}),
    "codestar": ("list_projects", {"maxResults": 1}),
    "config": ("describe_config_rules", {}),
    "datapipeline": ("list_pipelines", {}),
    "datasync": ("list_locations", {"MaxResults": 1}),
    "dax": ("describe_clusters", {"MaxResults": 20}),
    "directconnect": ("describe_direct_connect_gateways", {"maxResults": 1}),
    "dynamodb": ("list_tables", {"Limit": 1}),
    "ec2": ("describe_instances", {"MaxResults": 5}),
    "ecr": ("describe_repositories", {"maxResults": 1}),
    "ecs": ("list_clusters", {"maxResults": 1}),
    "efs": ("describe_file_systems", {"MaxItems": 1}),
    "eks": ("list_clusters", {"maxResults": 1}),
    "elasticache": ("describe_cache_clusters", {"MaxRecords": 20}),
    "elasticbeanstalk": ("describe_environments", {"MaxRecords": 1}),
    "elb": ("describe_load_balancers", {"PageSize": 1}),
    "elbv2": ("describe_load_balancers", {"PageSize": 1}),
    "emr": ("list_clusters", {}),
    "es": ("list_domain_names", {}),
    "events": ("list_event_buses", {"Limit": 1}),
    "firehose": ("list_delivery_streams", {"Limit": 1}),
    "fms": ("list_member_accounts", {"MaxResults": 1}),
    "glacier": ("list_vaults", {"limit": "1"}),
    "glue": ("list_jobs", {"MaxResults": 1}),
    "guardduty": ("list_detectors", {"MaxResults": 1}),
    "iam": ("list_roles", {"MaxItems": 1}),
    "inspector": ("list_findings", {"maxResults": 1}),
    "kafka": ("list_clusters", {"MaxResults": 1}),
    "kinesis": ("list_streams", {"Limit": 1}),
    "kms": ("list_aliases", {"Limit": 1}),
    "lambda": ("list_functions", {"MaxItems": 1}),
    "logs": ("describe_log_groups", {"limit": 1}),
    #"macie": ("list_member_accounts", {"maxResults": 1}),
    
    "organizations": ("list_accounts", {"MaxResults": 1}),
    "rds": ("describe_db_instances", {"MaxRecords": 20}),
    "redshift": ("describe_clusters", {"MaxRecords": 20}),
    "route53": ("list_hosted_zones", {"MaxItems": "1"}),
    "route53resolver": ("list_resolver_endpoints", {"MaxResults": 1}),
    "s3": ("list_buckets", {"Buckets": []}),
    "secretsmanager": ("list_secrets", {"MaxResults": 1}),
    "sns": ("list_topics", {}),
    "sqs": ("list_queues", {}),
    "ssm": ("list_commands", {"MaxResults": 1}),
    "storagegateway": ("list_gateways", {"Limit": 1}),
    "waf": ("list_rules", {"Limit": 1}),
    "waf-regional": ("list_rules", {"Limit": 1}),
    "wafv2": ("list_ip_sets", {"Limit": 1}),
    "workspaces": ("describe_workspaces", {"Limit": 1}),
    "xray": ("get_sampling_rules", {}),
}


def check_aws_apis(session, service, aws_region):
    services = session.get_available_services() if service is None else [service]
    for service in services:
        if service not in API_TESTS:
            continue

        regions = session.get_available_regions(service) if aws_region == "all" else [aws_region]
        for region in regions:
            logging.debug(f"Checking {service} {region}")
            try:
                client = session.client(service, region_name=region)
                func_name, params = API_TESTS[service]
                response = getattr(client, func_name)(**params)

                logging.debug(response)
                assert response["ResponseMetadata"]["HTTPStatusCode"] == 200
                print(f'{service} ({region}): {response["ResponseMetadata"]["HTTPStatusCode"]}')
    
            except ClientError as e:
                error_code = e.response["Error"]["Code"]
                if error_code == "InternalError":
                    logging.error(f"AWS {service} API Internal Error: {e}")
                elif error_code in ["AuthFailure", "UnrecognizedClientException"]:
                    logging.warning(f"Failed to test region {region}: {error_code}")
                elif error_code in ["AccessDenied", "AccessDeniedException"]:
                    logging.warning(f"Failed to test {service}: {e}")
                else:
                    logging.error(f"Failed to test {service}: {error_code}")
                    raise
            except Exception as e:
                logging.error(e)


@click.command()
@click.option("--listservices", "-l", is_flag=True,
              help="List all services of the region associated to the given profile.")
@click.option("--profile", "-p", help="AWS profile name.")
@click.option("--region", "-r", default="ap-southeast-2", help="AWS Region; use 'all' for all regions.")
@click.option("--service", "-s", default=None,
              help="(Optional) Service to be tested; if not specified, all services supported will be tested.")
def main(profile, service, region, listservices):
    try:
        session = Session(profile_name=profile)
        
        if listservices:
            print(session.get_available_services())
        else:
            check_aws_apis(session, service, region)

    except ClientError as e:
        if e.response["Error"]["Code"] == "ExpiredToken":
            logging.warning(f"{profile} token expired. Aborted")
        else:
            raise


if __name__ == "__main__": main()

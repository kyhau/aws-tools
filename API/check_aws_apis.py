"""
A script to check some AWS APIs current status.
"""
from boto3.session import Session
from botocore.exceptions import ClientError
import click
import logging

logging.getLogger().setLevel(logging.INFO)

API_TESTS = {
    # service: [(func_name, {params}, [validation_funcs]]
    "acm": [("list_certificates", {"MaxItems": 1}, [lambda x: len(x["CertificateSummaryList"]) > 0])],
    "apigateway": [("get_rest_apis", {"limit": 1}, None)],
    "apigatewayv2": [("get_apis", {"MaxResults": "1"}, None)],
    "athena": [("list_work_groups", {}, None)],
    "autoscaling": [("describe_auto_scaling_instances", {"MaxRecords": 1}, None)],
    "backup": [("list_backup_jobs", {"MaxResults": 1}, None)],
    "cloudformation": [("list_stacks", {}, None)],
    "cloudfront": [("list_distributions", {"MaxItems": "1"}, None)],
    "cloudtrail": [("describe_trails", {}, None)],
    "cloudwatch": [("describe_alarms", {"MaxRecords": 1}, None)],
    "codebuild": [("list_projects", {}, None)],
    "codecommit": [("list_repositories", {}, None)],
    "codedeploy": [("list_applications", {}, None)],
    "codepipeline": [("list_pipelines", {}, None)],
    "codestar": [("list_projects", {"maxResults": 1}, None)],
    "config": [("describe_config_rules", {}, None)],
    "datapipeline": [("list_pipelines", {}, None)],
    "datasync": [("list_locations", {"MaxResults": 1}, None)],
    "dax": [("describe_clusters", {"MaxResults": 20}, None)],
    "directconnect": [("describe_direct_connect_gateways", {"maxResults": 1}, None)],
    "dynamodb": [("list_tables", {"Limit": 1}, None)],
    "ec2": [
        ("describe_instances", {"MaxResults": 5}, [lambda x: len(x["Reservations"][0]["Instances"]) > 0]),
        ("describe_network_acls", {"MaxResults": 5}, [lambda x: len(x["NetworkAcls"][0]["Entries"]) > 0]),
        ("describe_route_tables", {"MaxResults": 5}, [lambda x: len(x["RouteTables"][0]["Routes"]) > 0]),
    ],
    "ecr": [("describe_repositories", {"maxResults": 1}, None)],
    "ecs": [("list_clusters", {"maxResults": 1}, None)],
    "efs": [("describe_file_systems", {"MaxItems": 1}, None)],
    "eks": [("list_clusters", {"maxResults": 1}, None)],
    "elasticache": [("describe_cache_clusters", {"MaxRecords": 20}, None)],
    "elasticbeanstalk": [("describe_environments", {"MaxRecords": 1}, None)],
    "elb": [("describe_load_balancers", {"PageSize": 1}, None)],
    "elbv2": [("describe_load_balancers", {"PageSize": 1}, None)],
    "emr": [("list_clusters", {}, None)],
    "es": [("list_domain_names", {}, None)],
    "events": [("list_event_buses", {"Limit": 1}, None)],
    "firehose": [("list_delivery_streams", {"Limit": 1}, None)],
    "fms": [("list_member_accounts", {"MaxResults": 1}, None)],
    "glacier": [("list_vaults", {"limit": "1"}, None)],
    "glue": [("list_jobs", {"MaxResults": 1}, None)],
    "guardduty": [("list_detectors", {"MaxResults": 1}, None)],
    "iam": [("list_roles", {"MaxItems": 1}, None)],
    "inspector": [("list_findings", {"maxResults": 1}, None)],
    "kafka": [("list_clusters", {"MaxResults": 1}, None)],
    "kinesis": [("list_streams", {"Limit": 1}, None)],
    "kms": [("list_aliases", {"Limit": 1}, None)],
    "lakeformation": [("list_resources", {"MaxResults": 1}, None)],
    "lambda": [("list_functions", {"MaxItems": 1}, None)],
    "logs": [("describe_log_groups", {"limit": 1}, None)],
    #"macie": [("list_member_accounts", {"maxResults": 1}, None)],
    "organizations": [("list_accounts", {"MaxResults": 1}, None)],
    "rds": [("describe_db_instances", {"MaxRecords": 20}, None)],
    "redshift": [("describe_clusters", {"MaxRecords": 20}, None)],
    "route53": [("list_hosted_zones", {"MaxItems": "1"}, None)],
    "route53resolver": [("list_resolver_endpoints", {"MaxResults": 1}, None)],
    "s3": [("list_buckets", {"Buckets": []}, None)],
    "secretsmanager": [("list_secrets", {"MaxResults": 1}, None)],
    "sns": [("list_topics", {}, None)],
    "sqs": [("list_queues", {}, None)],
    "ssm": [("list_commands", {"MaxResults": 1}, None)],
    "storagegateway": [("list_gateways", {"Limit": 1}, None)],
    "waf": [("list_rules", {"Limit": 1}, None)],
    "waf-regional": [("list_rules", {"Limit": 1}, None)],
    "wafv2": [("list_ip_sets", {"Limit": 1}, None)],
    "workspaces": [("describe_workspaces", {"Limit": 1}, None)],
    "xray": [("get_sampling_rules", {}, None)],
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
                
                for test_case in API_TESTS[service]:
                    func_name, params, resp_funcs = test_case
    
                    try:
                        response = getattr(client, func_name)(**params)
                        logging.debug(response)
                        status_code = response["ResponseMetadata"]["HTTPStatusCode"]
                        tests = [resp_func(response) for resp_func in resp_funcs] if resp_funcs is not None else []

                        print(f"{service}.{func_name} ({region}): {status_code}, tests:{tests}")
                        assert status_code == 200 and False not in tests

                    except ClientError as e:
                        error_code = e.response["Error"]["Code"]
                        if error_code == "InternalError":
                            logging.error(f"AWS {service}.{func_name} Internal Error: {e}")
                        elif error_code in ["AccessDenied", "AccessDeniedException"]:
                            logging.warning(f"Failed to test {service}: {e}")
                        else:
                            logging.error(f"Failed to test {service}.{func_name}: {error_code}")
                    except Exception as e:
                        logging.error(f"AWS {service}.{func_name} returns unexpected response: {e}")

            except ClientError as e:
                error_code = e.response["Error"]["Code"]
                if error_code in ["AuthFailure", "UnrecognizedClientException"]:
                    logging.warning(f"Failed to test region {region}: {error_code}")
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

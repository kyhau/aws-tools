#!/bin/bash
# https://aws.amazon.com/blogs/aws/new-query-for-aws-regions-endpoints-and-more-using-aws-systems-manager-parameter-store/
set -e

if [ "$1" = "-h" ] || [ "$1" = "--help" ] ; then
    echo "Usage: [ARGUMENTS] [-h|--help]
    ARGUMENTS:
      regions: list all global regions
      services: list all global services
      [REGION_NAME]: list all services of a region
      [SERVICE_NAME]: print the name of the service
      regions [SERVICE_NAME]: list all regions of a service
      [REGION_NAME] [SERVICE_NAME] endpoint: print the endpoint of [REGION_NAME]/services/[SERVICE_NAME]
    "
    return
fi

# List all global regions
[ "$#" = 1 ] && [ "$1" = "regions" ] && aws ssm get-parameters-by-path --path /aws/service/global-infrastructure/regions --output json | jq .Parameters[].Name | sort && return

# List all global services
[ "$#" = 1 ] && [ "$1" = "services" ] && aws ssm get-parameters-by-path --path /aws/service/global-infrastructure/services --output json | jq .Parameters[].Name | sort && return

# List all services of a region
[ "$#" = 1 ] && [[ "$1" = *"-"*"-"* ]] && aws ssm get-parameters-by-path --path /aws/service/global-infrastructure/regions/${1}/services --output json | jq .Parameters[].Name | sort && return

# Print the name of a service
[ "$#" = 1 ] && aws ssm get-parameters-by-path --path /aws/service/global-infrastructure/services/${1} --output json | jq .Parameters[].Value && return

# List all regions of a service
[ "$#" = 2 ] && [ "$1" = "regions" ] && aws ssm get-parameters-by-path --path /aws/service/global-infrastructure/services/${2}/regions --output json | jq .Parameters[].Value | sort && return

# Print the endpoint of a service in a region
[ "$#" = 3 ] && [ "$3" = "endpoint" ] && aws ssm get-parameter --name /aws/service/global-infrastructure/regions/${1}/services/${2}/endpoint --output json | jq .Parameter.Value && return

echo "Not sure what to do. Use -h to get help."

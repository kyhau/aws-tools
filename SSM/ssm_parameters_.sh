#!/bin/bash
# https://aws.amazon.com/blogs/aws/new-query-for-aws-regions-endpoints-and-more-using-aws-systems-manager-parameter-store/
set -e

echo $1
echo $2
echo "what"

help_menu() {
  echo "Usage:
  ${0##*/}
    --build-image                Build/test docker image.
    --build-number BUILD_NUMBER  The build number to uniquely identify the image we build. Default to 000.
  "
  exit
}

while [[ "$#" > 0 ]]; do case $1 in
    -r|--region)    region="${2}"   ; shift ;;
    -s|--service)   service="${2}"  ; shift ;;
    -h|--help)      help_menu               ;;
    *)            echo "Invalid option: ${1}" && help_menu ;;
esac; shift; done

#[[ ! -z "$BUILD_NUMBER" ]] || (echo "Error: BUILD_NUMBER is not provided. Aborted." && exit 1)

if [[ $region = "all" ]]; then
  aws ssm get-parameters-by-path --path /aws/service/global-infrastructure/regions --output json | jq .Parameters[].Name | sort
  exit 0
fi

aws ssm get-parameters-by-path --path /aws/service/global-infrastructure/services --output json | jq .Parameters[].Name | sort

aws ssm get-parameters-by-path --path /aws/service/global-infrastructure/regions/us-east-1/services --output json | jq .Parameters[].Name | sort

aws ssm get-parameters-by-path --path /aws/service/global-infrastructure/services/athena/regions --output json | jq .Parameters[].Value

# Here’s how to use the path to get the name of a service:

aws ssm get-parameters-by-path --path /aws/service/global-infrastructure/services/athena --output json | jq .Parameters[].Value
#"Amazon Athena"

# And here’s how you can find the regional endpoint for a given service, again using the path:

aws ssm get-parameter --name /aws/service/global-infrastructure/regions/us-west-1/services/s3/endpoint --output json | jq .Parameter.Value
# "s3.us-west-1.amazonaws.com"


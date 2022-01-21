#!/bin/bash
set -e

PROFILE="default"
REGION="ap-southeast-2"
STACK_NAME="UnhealthyWorkSpacesAlaram"
TO_EMAIL_ADDRESS="TODO"

# pip install -U awscli

aws cloudformation validate-template --template-body "file://unhealthy-workspaces-cloudwatch-alarms.yaml" --profile ${PROFILE}

aws cloudformation deploy --template-file unhealthy-workspaces-cloudwatch-alarms.yaml --stack-name ${STACK_NAME} \
  --parameter-overrides ToEmailAddress=${TO_EMAIL_ADDRESS} \
  --tags Billing=workspaces \
  --capabilities CAPABILITY_NAMED_IAM \
  --no-fail-on-empty-changeset \
  --region ${REGION} \
  --profile ${PROFILE}

# aws cloudformation delete-stack --stack-name ${STACK_NAME} --region ${REGION} --profile ${PROFILE}

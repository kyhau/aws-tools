#!/bin/bash
set -e

STACK_NAME=ApiGateway-CloudWatchLogs
TEMPLATE_FILE=ApiGateway-CloudWatchLogs.template.yaml

aws cloudformation validate-template --template-body file://${TEMPLATE_FILE}

aws cloudformation deploy --stack-name ${STACK_NAME} --template-file ${TEMPLATE_FILE} \
  --capabilities CAPABILITY_NAMED_IAM \
  --tags Billing=${STACK_NAME}

echo "Outputs:"
aws cloudformation describe-stacks --stack-name ${STACK_NAME} --query "Stacks[0].Outputs"

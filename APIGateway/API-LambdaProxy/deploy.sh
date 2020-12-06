#!/bin/bash
set -e

API_NAME=K-LambdaProxy-API
TEMPLATE_FILE=Apigw-LambdaProxy.template.yaml

aws cloudformation validate-template --template-body file://${TEMPLATE_FILE}

aws cloudformation deploy --stack-name ${API_NAME} --template-file ${TEMPLATE_FILE} \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides ApiName=${API_NAME} ApiStageName=v0 \
  --tags Billing=${API_NAME}

echo "APIGW URL:"
aws cloudformation describe-stacks --stack-name ${API_NAME} --query "Stacks[0].Outputs[0].OutputValue" --output text

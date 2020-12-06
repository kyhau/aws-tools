#!/bin/bash
set -e

API_NAME=K-LambdaProxy-API
TEMPLATE_FILE=Apigw-LambdaProxy.template.yaml

echo "Valdating template..."
aws cloudformation validate-template --template-body file://${TEMPLATE_FILE}

echo "Deploying CloudFormation stack..."
aws cloudformation deploy --stack-name ${API_NAME} --template-file ${TEMPLATE_FILE} \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides ApiName=${API_NAME} ApiStageName=v0 \
  --tags Billing=${API_NAME}

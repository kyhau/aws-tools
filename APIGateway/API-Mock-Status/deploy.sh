#!/bin/bash
set -e

API_NAME=K-Mock-Status-API
TEMPLATE_FILE=Apigw-Mock-Status.template.yaml

echo "Valdating template..."
aws cloudformation validate-template --template-body file://${TEMPLATE_FILE}

echo "Deploying CloudFormation stack..."
aws cloudformation deploy --stack-name ${API_NAME} --template-file ${TEMPLATE_FILE} \
  --parameter-overrides ApiName=${API_NAME} ApiStageName=v0 \
  --tags Billing=${API_NAME}

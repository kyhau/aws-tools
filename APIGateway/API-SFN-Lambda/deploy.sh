#!/bin/bash
set -e

API_NAME=K-SFN-API
TEMPLATE_FILE=Apigw-Sfn-Lambda.template.yaml

echo "Valdating template..."
aws cloudformation validate-template --template-body file://${TEMPLATE_FILE}

echo "Deploying CloudFormation stack..."
aws cloudformation deploy --stack-name ${API_NAME} --template-file ${TEMPLATE_FILE} \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides ApiName=${API_NAME} \
  --tags Billing=${API_NAME}

#!/bin/bash
set -e

API_NAME=K-Mock-Simple-API
TEMPLATE_FILE=Apigw-Mock-Simple.template.yaml

aws cloudformation validate-template --template-body file://${TEMPLATE_FILE}

aws cloudformation deploy --stack-name ${API_NAME} --template-file ${TEMPLATE_FILE} \
  --parameter-overrides ApiGatewayName=${API_NAME} StageName=v0 \
  --tags Billing=${API_NAME}

echo "APIGW URL:"
aws cloudformation describe-stacks --stack-name ${API_NAME} --query "Stacks[0].Outputs[0].OutputValue" --output text

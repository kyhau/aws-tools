#!/bin/bash
set -e

API_NAME=K-Mock-Status-API

aws cloudformation validate-template --template-body file://Apigw-Mock-Status.template.yaml

aws cloudformation deploy --stack-name ${API_NAME} --template-file Apigw-Mock-Status.template.yaml \
  --parameter-overrides ApiGatewayName=${API_NAME} StageName=v0 \
  --tags Billing=${API_NAME}

echo "APIGW URL:"
aws cloudformation describe-stacks --stack-name ${API_NAME} --query "Stacks[0].Outputs[0].OutputValue" --output text

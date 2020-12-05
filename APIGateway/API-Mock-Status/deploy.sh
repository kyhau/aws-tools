#!/bin/bash
set -e

API_NAME=K-Mock-Status-API

aws cloudformation validate-template --template-body file://Apigw-Mock-Status.template.yaml

aws cloudformation deploy --stack-name ${API_NAME} --template-file Apigw-Mock-Status.template.yaml \
  --parameter-overrides ApiGatewayName=${API_NAME} StageName=v0 \
  --tags Billing=${API_NAME}

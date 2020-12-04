#!/bin/bash
set -e

aws cloudformation validate-template --template-body file://Apigw-Mock.template.yaml

aws cloudformation deploy --stack-name K-APIGW-Mock --template-file Apigw-Mock.template.yaml \
  --parameter-overrides ApiGatewayName=K-Mock-API StageName=v0 \
  --tags Billing=K-APIGW-Mock

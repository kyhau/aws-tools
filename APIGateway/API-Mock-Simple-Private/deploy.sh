#!/bin/bash
set -e

# TODO - Update details of subnets (Mappings in Apigw-VpcEndpoint.template.yaml)
# TODO - Update VPC_ID below
VPC_ID=vpc-12345678

API_NAME=K-Mock-Simple-Private-API


ENDPOINT_STACK_NAME=K-Mock-Simple-APIGW-VpcEndpoint
TEMPLATE_FILE_=Apigw-VpcEndpoint.template.yaml

echo "Valdating template..."
aws cloudformation validate-template --template-body file://${TEMPLATE_FILE}

echo "Deploying CloudFormation stack ${ENDPOINT_STACK_NAME}..."

aws cloudformation deploy --stack-name ${ENDPOINT_STACK_NAME} --template-file ${TEMPLATE_FILE} \
  --parameter-overrides VpcId=${VPC_ID} \
  --tags Billing=${API_NAME}

VpcEndpointId=$(aws cloudformation describe-stacks --stack-name ${ENDPOINT_STACK_NAME} --query "Stacks[0].Outputs[3].OutputValue" --output text)
echo "VpcEndpointId: ${VpcEndpointId}"


TEMPLATE_FILE=Apigw-Mock-Simple.template.yaml

echo "Valdating template..."
aws cloudformation validate-template --template-body file://${TEMPLATE_FILE}

echo "Deploying CloudFormation stack ${API_NAME}..."

aws cloudformation deploy --stack-name ${API_NAME} --template-file ${TEMPLATE_FILE} \
  --parameter-overrides ApiName=${API_NAME} ApiStageName=v0 VpcEndpointId=${VpcEndpointId} VpcId=${VPC_ID} \
  --tags Billing=${API_NAME}

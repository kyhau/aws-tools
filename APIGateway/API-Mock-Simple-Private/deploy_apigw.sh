#!/bin/bash
set -e

# TODO - Update details of subnets (Mappings in Apigw-VpcEndpoint.template.yaml)
# TODO - Update VPC_ID below
VPC_ID=vpc-12345678

API_NAME=K-Mock-Simple-Private-API

################################################################
VPCE_STACK_NAME=K-Mock-Simple-APIGW-VpcEndpoint
TEMPLATE_FILE_1=Apigw-VpcEndpoint.template.yaml

echo "Valdating template..."
aws cloudformation validate-template --template-body file://${TEMPLATE_FILE_1}

echo "Deploying CloudFormation stack ${VPCE_STACK_NAME}..."

aws cloudformation deploy --stack-name ${VPCE_STACK_NAME} --template-file ${TEMPLATE_FILE_1} \
  --parameter-overrides VpcId=${VPC_ID} \
  --tags Billing=${API_NAME}

VpcEndpointId=$(aws cloudformation describe-stacks --stack-name ${VPCE_STACK_NAME} --query "Stacks[0].Outputs[3].OutputValue" --output text)
echo "VpcEndpointId: ${VpcEndpointId}"

################################################################
APIGW_STACK_NAME=K-Mock-Simple-Private-API
TEMPLATE_FILE_2=Apigw-Mock-Simple.template.yaml

echo "Valdating template..."
aws cloudformation validate-template --template-body file://${TEMPLATE_FILE_2}

echo "Deploying CloudFormation stack ${APIGW_STACK_NAME}..."

aws cloudformation deploy --stack-name ${APIGW_STACK_NAME} --template-file ${TEMPLATE_FILE_2} \
  --parameter-overrides ApiName=${API_NAME} ApiStageName=v0 VpcEndpointId=${VpcEndpointId} VpcId=${VPC_ID} \
  --tags Billing=${API_NAME}

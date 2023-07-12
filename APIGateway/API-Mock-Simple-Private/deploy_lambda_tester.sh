#!/bin/bash
set -e

# TODO - Update details of subnets (Mappings in Lambda-ApiTester.template.yaml)
# TODO - Update VPC_ID below
VPC_ID=vpc-12345678

# TODO: Copy first dns from the stack "VPCE_STACK_NAME" output "VpcEndpointDnsEntries"
VPCE_PUBLIC_DNS_NAME=VPCE_ID-xxxxxxxx.execute-api.REGION.vpce.amazonaws.com

# TODO: Copy outputs from the stack "APIGW_STACK_NAME"
APIGW_ENDPOINT=API_ID.execute-api.REGION.amazonaws.com
APIGW_VPCE_R53_Alias=API_ID-VPCE_ID.execute-api.REGION.amazonaws.com
API_PATH=/v0/mock

################################################################
API_NAME=K-Mock-Simple-Private-API
LAMBDA_STACK_NAME=K-Mock-Simple-Private-API-LambdaTester
TEMPLATE_FILE=Lambda-ApiTester.template.yaml

echo "Valdating template..."
aws cloudformation validate-template --template-body file://${TEMPLATE_FILE}

echo "Deploying CloudFormation stack ${LAMBDA_STACK_NAME}..."

aws cloudformation deploy --stack-name ${LAMBDA_STACK_NAME} --template-file ${TEMPLATE_FILE} \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides ApigwEndpoint=${APIGW_ENDPOINT} \
      ApigwVpcEndpointR53Alias=${APIGW_VPCE_R53_Alias} \
      VpcEndpointPublicDnsName=${VPCE_PUBLIC_DNS_NAME} \
      ApiPath=${API_PATH} \
      VpcId=${VPC_ID} \
  --tags Billing=${API_NAME}


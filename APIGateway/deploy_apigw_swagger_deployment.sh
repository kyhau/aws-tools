#!/bin/bash
set -e

aws cloudformation validate-template --template-body file://Apigw-Sfn-Lambda.template.yaml


echo "Deploying CloudFormation stack..."

aws cloudformation deploy --stack-name K-SFN-API --template-file Apigw-Sfn-Lambda.template.yaml \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides ApigwName=K-SFN-API \
  --tags Billing=K-SFN-API


API_ID=todo_api_id
ACCOUNT_ID=1231456789012
SFN_ARN=arn:aws:states:ap-southeast-2:1231456789012:stateMachine:K-SFN-StateMachine

REGION=ap-southeast-2
STAGE=v0

echo "Updating swagger file..."

cp API-swagger.yaml API-swagger-2.yaml

ESCAPED_REPLACE=$(printf '%s\n' "$API_ID" | sed -e 's/[\/&]/\\&/g')
sed -i "s/todo_api_id/$ESCAPED_REPLACE/g" API-swagger-2.yaml

ESCAPED_REPLACE=$(printf '%s\n' "$REGION" | sed -e 's/[\/&]/\\&/g')
sed -i "s/todo_region/$ESCAPED_REPLACE/g" API-swagger-2.yaml

ESCAPED_REPLACE=$(printf '%s\n' "$ACCOUNT_ID" | sed -e 's/[\/&]/\\&/g')
sed -i "s/1231456789012/$ESCAPED_REPLACE/g" API-swagger-2.yaml


echo "Deploying swagger file..."

aws apigateway put-rest-api --rest-api-id ${API_ID} --mode overwrite --body 'file://API-swagger-2.yaml'


echo "Creating new deployment..."

aws apigateway create-deployment --rest-api-id ${API_ID} --stage-name ${STAGE} \
  --variables sfnArn="${SFN_ARN}" \
  --stage-description "Stage ${STAGE}" --description "Deployment to the ${STAGE}"

rm API-swagger-2.yaml

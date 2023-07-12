#!/bin/bash

STAGE=${1:-dev}
REGION=${2:-ap-southeast-2}

echo "STAGE is: ${STAGE}"
echo "REGION is: ${REGION}"

APIGW_ID=$(aws cloudformation list-exports --region ${REGION} --query "Exports[?Name=='APIGW-ID-${STAGE}'].Value" --output text)
CW_LOGGROUP_NAME="API-Gateway-Execution-Logs_${APIGW_ID}/${STAGE}"
CW_LOGGROUP_RETENTION_IN_DAYS=90


if [[ -z "$APIGW_ID" ]]; then
	echo "Could not find APIGW-ID-${STAGE}"
else
	echo "REST API is: ${APIGW_ID}"

  if [[ $STAGE != "prd"* ]]; then
    CW_LOGGROUP_RETENTION_IN_DAYS=5
  fi

  # 1. Set Log level: OFF, ERROR, or INFO
  # 2. Disable full request/response logging for all resources/methods in an API stage
  # 3. Enable CloudWatch metric
  # 4. Enable X-Ray tracing
  aws apigateway update-stage --rest-api-id ${APIGW_ID} --stage-name ${STAGE} --region ${REGION} \
    --patch-operations \
      "op='replace',path='/*/*/logging/loglevel',value='INFO'" \
      "op='replace',path='/*/*/logging/dataTrace',value='false'" \
      "op='replace',path='/*/*/metrics/enabled',value='true'" \
      "op='replace',path='/tracingEnabled',value='true'"

  # Set the retention (days) for the CloudWatch Loggroup of the API Gateway stage
  aws logs put-retention-policy --log-group-name ${CW_LOGGROUP_NAME} --retention-in-days ${CW_LOGGROUP_RETENTION_IN_DAYS} --region ${REGION}
fi

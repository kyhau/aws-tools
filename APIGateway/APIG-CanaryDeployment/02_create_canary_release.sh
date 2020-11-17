#!/bin/bash
set -e

APIG_ID=todo_apig_id

# Create a canary deployment on the prod stage

aws apigateway create-deployment --rest-api-id ${APIG_ID} --stage-name prod --tracing-enabled \
  --canary-settings '{
      "percentTraffic":100.0,
      "useStageCache":false,
      "stageVariableOverrides":{
          "lambdaAlias":"green",
          "sfnArn":"arn:aws:states:ap-southeast-2:1231456789012:stateMachine:K-SFN-StateMachine-Green"
      }
  }'


echo "CheckPt"
aws apigateway get-stage --rest-api-id ${APIG_ID} --stage-name prod
# deploymentId returned is that of baseline, not canary's

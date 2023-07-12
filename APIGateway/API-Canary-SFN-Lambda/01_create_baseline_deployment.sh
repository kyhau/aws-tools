#!/bin/bash
set -e

APIG_ID=todo_apig_id
SFN_1_ARN='arn:aws:states:ap-southeast-2:1231456789012:stateMachine:K-SFN-StateMachine-Blue'

aws apigateway create-deployment --rest-api-id ${APIG_ID} --stage-name prod --tracing-enabled --variables sfnArn=${SFN_1_ARN},lambdaAlias=blue

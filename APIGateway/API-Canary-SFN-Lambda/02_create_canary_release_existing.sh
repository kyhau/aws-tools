#!/bin/bash
set -e

APIG_ID=todo_apig_id

# create a new canary release deployment by attaching a canary on the stage:

aws apigateway update-stage --rest-api-id ${APIG_ID} --stage-name prod \
    --patch-operations '[{
        "op":"replace",
        "path":"/canarySettings/percentTraffic",
        "value":"100.0"
    },{
        "op":"replace",
        "path":"/canarySettings/useStageCache",
        "value":"false"
    },{
        "op":"replace",
        "path":"/canarySettings/stageVariableOverrides/sfnArn",
        "value":"arn:aws:states:ap-southeast-2:1231456789012:stateMachine:K-SFN-StateMachine-Green"
    },{
        "op":"replace",
        "path":"/canarySettings/stageVariableOverrides/lambdaAlias",
        "value":"green"
    }]'


echo "CheckPt"
aws apigateway get-stage --rest-api-id ${APIG_ID} --stage-name prod
# deploymentId returned is that of baseline, not canary's
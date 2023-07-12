#!/bin/bash
set -e

# https://docs.aws.amazon.com/apigateway/latest/developerguide/promote-canary-deployment.html

APIG_ID=todo_apig_id

aws apigateway update-stage --rest-api-id ${APIG_ID} --stage-name prod \
  --patch-operations '[{
      "op": "replace",
      "value": "0.0"
      "path": "/canarySettings/percentTraffic",
    }, {
      "op": "copy",
      "from": "/canarySettings/stageVariableOverrides",
      "path": "/variables",
    }, {
      "op": "copy",
      "from": "/canarySettings/deploymentId",
      "path": "/deploymentId"
    }]'

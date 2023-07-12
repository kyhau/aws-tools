#!/bin/bash
set -e

# https://docs.aws.amazon.com/apigateway/latest/developerguide/delete-canary-deployment.html

APIG_ID=todo_apig_id

aws apigateway update-stage --rest-api-id ${APIG_ID} --stage-name prod \
    --patch-operations '[{"op":"remove", "path":"/canarySettings"}]'

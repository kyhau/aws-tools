#!/bin/bash
set -e

API_NAME=K-SFN-API

API_URL=$(aws cloudformation describe-stacks --stack-name ${API_NAME} --query "Stacks[0].Outputs[0].OutputValue" --output text)
echo "API URL: ${API_URL}"

echo "Start execution"
date
eid=$(curl -X POST ${API_URL} | jq --raw-output '.token')
echo

echo "Check execution status: ${eid}"
date
curl -X GET ${API_URL}/?eid=${eid}
echo

#!/bin/bash
# Set to fail script if any command fails.
set -e

AWS_PROFILE="default"
SESSION_NAME="testing"
ROLE_ARN="arn:aws:iam::123456789012:role/DEV-01"

resp=$(aws sts assume-role --role-arn "$ROLE_ARN" --profile "$AWS_PROFILE" --role-session-name "$SESSION_NAME")
AWS_ACCESS_KEY_ID=$(echo "$resp" | jq -r '.Credentials.AccessKeyId')
AWS_SECRET_ACCESS_KEY=$(echo "$resp" | jq -r '.Credentials.SecretAccessKey')
AWS_SESSION_TOKEN=$(echo "$resp" | jq -r '.Credentials.SessionToken')

cat >> ~/.aws/credentials << EOL

[${SESSION_NAME}]
aws_access_key_id = ${AWS_ACCESS_KEY_ID}
aws_secret_access_key = ${AWS_SECRET_ACCESS_KEY}
aws_session_token =  ${AWS_SESSION_TOKEN}

EOL

#!/bin/bash
# Set to fail script if any command fails.
set -e

AWS_PROFILE=""
SESSION_NAME="test-s3"
ROLE_ARN="arn:aws:iam::111122223333:role/s3-bucket-readonly-role"

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

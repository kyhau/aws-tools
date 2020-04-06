#!/bin/bash

ROLE_NAME=
POLICY_ARN="arn:aws:iam::012345678987:policy/ec2_ip_policy"
AWS_REGION=${AWS_DEFAULT_REGION:=ap-southeast-2}

cat > lambda_function.py << EOL
import boto3
def lambda_handler(event, context):
    policy = boto3.client("iam")
    resp = policy.attach_role_policy(
      RoleName="${ROLE_NAME}",
      PolicyArn="${POLICY_ARN}",
    )
EOL

zip lambda_function.zip lambda_function.py

aws lambda create-function \
  --function-name "lambda_function" \
  --zip-file "fileb://lambda_function.zip" \
  --handler "lambda_function.lambda_handler" \
  --runtime "python3.7" \
  --role "$ROLE_ARN" \
  --region "$AWS_REGION" \
  --tracing-config "Active"

rm lambda_function.py lambda_function.zip

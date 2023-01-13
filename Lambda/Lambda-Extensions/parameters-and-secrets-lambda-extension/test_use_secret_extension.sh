#!/bin/bash
set -e

# https://docs.aws.amazon.com/secretsmanager/latest/userguide/retrieving-secrets_lambda.html

cdk init app --language python

aws secretsmanager create-secret --name MyTestSecret --secret-string HelloWorldTestCase1

zip use_secret_extension.zip use_secret_extension.py

# arn:aws:lambda:ap-southeast-2:665172237481:layer:AWS-Parameters-and-Secrets-Lambda-Extension
# arn:aws:lambda:ap-southeast-2:665172237481:layer:AWS-Parameters-and-Secrets-Lambda-Extension-Arm64

aws lambda update-function-configuration \
    --function-name use_secret_extension \
    --layers arn:aws:lambda:ap-southeast-2:665172237481:layer:AWS-Parameters-and-Secrets-Lambda-Extension

rm use_secret_extension.zip

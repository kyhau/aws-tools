#!/bin/bash
# Set to fail script if any command fails.
set -e

aws serverlessrepo create-cloud-formation-template --application-id arn:aws:serverlessrepo:us-east-1:903779448426:applications/lambda-layer-awscli

# Copy the TemplateUrl value and deploy with cloudformation create-stack

STACK_NAME=TODO

aws cloudformation create-stack --template-url {TemplateUrl} --stack-name "$STACK_NAME" --capabilities CAPABILITY_AUTO_EXPAND


aws cloudformation describe-stacks --stack-name "$STACK_NAME" --query 'Stacks[0].Outputs'
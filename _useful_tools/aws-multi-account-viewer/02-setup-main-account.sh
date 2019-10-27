#!/bin/bash
# Set to fail script if any command fails.
set -e

# TODO - fill in the TODOs
REPO_HOME=TODO-1/aws-multi-account-viewer

AWS_PROFILE=TODO-2

# ID of the main aws account
MAIN_ACCOUNT=TODO-3

# Bucket to be created in the main aws account
MAIN_ACCOUNT_BUCKET=TODO-4

MAIN_ACCOUNT_DDB_TABLE=TODO-5

# String of IDs of the main aws account separated by commas
SUB_ACCOUNT_IDS=TODO-6


################################################################################
ORI_DIR=$(pwd)

function finish {
  # [[ -f tmp.json ]] && rm tmp.json
  cd "$ORI_DIR"
  echo "Goodbye"
}
trap finish EXIT

################################################################################
echo "Create a new S3 bucket to store the lambda zip files"

aws s3 mb s3://${MAIN_ACCOUNT_BUCKET} --profile $AWS_PROFILE

echo "Package up all the lambdas into one zip file"

cd ${REPO_HOME}/Back-End/lambdas
python3.7 -m venv .venv
source .venv/bin/activate
cd build
pip install -r ../requirements.txt --target .
zip -r9 ../functions.zip .
cd ../
zip -g functions.zip list_table.py receive_sqs_message.py send_sqs_message.py
deactivate

echo "Copy the functions.zip file you just packaged into the s3 bucket created"

aws s3 cp functions.zip s3://${MAIN_ACCOUNT_BUCKET}

################################################################################
aws cloudformation create-stack --stack-name Multi-account-viewer \
  --template-body file://${REPO_HOME}/Back-End/cloudformation/MainTemplate.yaml \
  --parameters ParameterKey=SourceAccount,ParameterValue=${MAIN_ACCOUNT} \
  --profile ${AWS_PROFILE}


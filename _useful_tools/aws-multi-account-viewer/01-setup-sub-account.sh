#!/bin/bash
# This script clone the repo first, then starts deploy CloudFormation stacks to the sub accounts

# Set to fail script if any command fails.
set -e

# TODO - fill in the TODOs
REPO_HOME=TODO-1/aws-multi-account-viewer

AWS_PROFILE=TODO-2

# ID of the main aws account
MAIN_ACCOUNT=TODO-3

# AWS Profiles of the sub accounts to be monitored
declare -a SUB_ACCOUNT_PROFILES=(
  "TODO-4a"
  "TODO-4b"
)

################################################################################
[[ -d "$REPO_HOME" ]] || git clone https://github.com/awslabs/aws-multi-account-viewer "$REPO_HOME"

for sub_account_profile in "${SUB_ACCOUNT_PROFILES[@]}"
do
  echo "$sub_account_profile"
  aws cloudformation create-stack --stack-name Multi-account-viewer-sub-account-access \
    --template-body file://${REPO_HOME}/Back-End/cloudformation/SubAccountAccess.yaml \
    --parameters ParameterKey=AdministratorAccountId,ParameterValue=${MAIN_ACCOUNT} \
    --profile ${sub_account_profile}
done

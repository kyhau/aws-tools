#!/bin/bash
set -e

source .env

AWS_PROFILE=${AWS_PROFILE_3}
REPO_NAME=${ACCOUNT_3_TEAM_3_REPO}

aws codeartifact login --tool pip --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} \
  --repository ${REPO_NAME} --profile ${AWS_PROFILE}

cat ~/.config/pip/pip.conf

echo "CheckPt: pip3 install boto3"
pip3 install boto3

rm ~/.config/pip/pip.conf

# Test - xx_list_packages.sh
# Test - xx_list_packages_in_external_repos.sh

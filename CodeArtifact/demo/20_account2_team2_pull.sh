#!/bin/bash
set -e

source .env

# Access a domain owned by an account you are authenticated to:

AWS_PROFILE=${AWS_PROFILE_2}
REPO_NAME=${ACCOUNT_2_TEAM_2_REPO}

# aws codeartifact list-package-versions --domain ${DOMAIN} --domain-owner ${ACCOUNT_2_ID} \
#  --repository ${REPO_NAME} --format pypi --package boto3 --profile ${AWS_PROFILE_2}

aws codeartifact login --tool pip --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} \
  --repository ${REPO_NAME} --profile ${AWS_PROFILE}

cat ~/.config/pip/pip.conf

echo "CheckPt: pip3 install boto3"
pip3 install boto3

rm ~/.config/pip/pip.conf

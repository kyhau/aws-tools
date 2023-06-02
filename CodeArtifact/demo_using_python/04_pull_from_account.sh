#!/bin/bash

source .config

# Access a domain owned by an account you are authenticated to:

export REPO_NAME="team-2-dev"

# aws codeartifact list-package-versions --domain ${DOMAIN} --domain-owner ${ACCOUNT_2_ID} \
#  --repository ${REPO_NAME} --format pypi --package boto3 --profile ${AWS_PROFILE_2}

aws codeartifact login --tool pip --domain ${DOMAIN} --domain-owner ${ACCOUNT_2_ID} \
  --repository ${REPO_NAME} --profile ${AWS_PROFILE_2}

cat ~/.config/pip/pip.conf

echo "TODO: pip install boto3"
# pip install boto3
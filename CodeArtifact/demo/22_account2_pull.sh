#!/bin/bash

source .env

# Access a domain owned by an account you are authenticated to:

export REPO_NAME=${ACCOUNT_1_SHARED_REPO_1}

# aws codeartifact list-package-versions --domain ${DOMAIN} --domain-owner ${ACCOUNT_2_ID} \
#  --repository ${REPO_NAME} --format pypi --package boto3 --profile ${AWS_PROFILE_2}

aws codeartifact login --tool pip --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} \
  --repository ${REPO_NAME} --profile ${AWS_PROFILE_2}

cat ~/.config/pip/pip.conf

echo "TODO: pip install boto3"
# pip install boto3

rm ~/.config/pip/pip.conf

#!/bin/bash
set -e

source .env

echo "CheckPt: account 2: list-packages domain account 1"
aws codeartifact list-packages --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} --repository ${ACCOUNT_1_SHARED_REPO_1} --profile ${AWS_PROFILE_2}

echo "CheckPt: account 2: list-packages domain account 2"
aws codeartifact list-packages --domain ${DOMAIN} --domain-owner ${ACCOUNT_2_ID} --repository ${ACCOUNT_2_REPO_1} --profile ${AWS_PROFILE_2}

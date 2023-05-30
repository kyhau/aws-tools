#!/bin/bash
set -e

source .env

echo "CheckPt: account 1: list-packages"
aws codeartifact list-packages --domain ${DOMAIN} --repository ${ACCOUNT_1_SHARED_REPO_1} --profile ${AWS_PROFILE_1}

echo "CheckPt: account 2: list-packages"
aws codeartifact list-packages --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} --repository ${ACCOUNT_1_SHARED_REPO_1} --profile ${AWS_PROFILE_2}

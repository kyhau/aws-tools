#!/bin/bash
set -e

source .env

echo "CheckPt: account 1: list-packages ${ACCOUNT_1_SHARED_REPO_1}"
aws codeartifact list-packages --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} --repository ${ACCOUNT_1_SHARED_REPO_1} --profile ${AWS_PROFILE_1}

echo "CheckPt: account 2: list-packages ${ACCOUNT_2_TEAM_2_REPO}"
aws codeartifact list-packages --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} --repository ${ACCOUNT_2_TEAM_2_REPO} --profile ${AWS_PROFILE_2}

echo "CheckPt: account 3: list-packages ${ACCOUNT_3_TEAM_3_REPO}"
aws codeartifact list-packages --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} --repository ${ACCOUNT_3_TEAM_3_REPO} --profile ${AWS_PROFILE_3}

# echo "CheckPt: account 3: list-packages ${ACCOUNT_2_TEAM_2_REPO}"
# aws codeartifact list-packages --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} --repository ${ACCOUNT_2_TEAM_2_REPO} --profile ${AWS_PROFILE_3}

# echo "CheckPt: account 2: list-packages ${ACCOUNT_3_TEAM_3_REPO}"
# aws codeartifact list-packages --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} --repository ${ACCOUNT_3_TEAM_3_REPO} --profile ${AWS_PROFILE_2}

#!/bin/bash
set -e

source .env

# Create repo in account 1 with domain owner 2

aws codeartifact create-repository --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} \
  --repository ${ACCOUNT_2_REPO_1} --description "My new repository" --profile ${AWS_PROFILE_2}

#!/bin/bash
set -e

source .env

aws codeartifact create-repository --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} \
  --repository ${ACCOUNT_1_SHARED_REPO_1} --description "My new repository" --profile ${AWS_PROFILE_1}

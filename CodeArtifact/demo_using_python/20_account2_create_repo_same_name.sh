#!/bin/bash
set -e

source .env

aws codeartifact create-repository --domain ${DOMAIN} --domain-owner ${ACCOUNT_2_ID} \
  --repository ${ACCOUNT_2_REPO_1} --description "My new repository" --profile ${AWS_PROFILE_2}

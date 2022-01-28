#!/bin/bash

source .config

# Create repo in account 2 with domain owner 2

aws codeartifact create-repository --domain ${DOMAIN} --domain-owner ${ACCOUNT_2_ID} \
  --repository ${ACCOUNT_2_REPO_1} --description "My new repository" --profile ${AWS_PROFILE_2}

aws codeartifact create-repository --domain ${DOMAIN} --domain-owner ${ACCOUNT_2_ID} \
  --repository ${ACCOUNT_2_REPO_2} --description "My new repository" --profile ${AWS_PROFILE_2}

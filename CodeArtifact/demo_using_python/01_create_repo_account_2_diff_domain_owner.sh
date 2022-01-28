#!/bin/bash

source .config

# Create repo in account 2 but with domain owner 1

aws codeartifact create-repository --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} \
  --repository ${ACCOUNT_2_SHARED_REPO_1} --description "My new repository" --profile ${AWS_PROFILE_2}

aws codeartifact create-repository --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} \
  --repository ${ACCOUNT_2_SHARED_REPO_2} --description "My new repository" --profile ${AWS_PROFILE_2}


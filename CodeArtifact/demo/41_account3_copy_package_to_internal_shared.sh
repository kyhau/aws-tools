#!/bin/bash
# Copy packages between repositories
# https://docs.aws.amazon.com/codeartifact/latest/ug/copy-package.html

source .env

###
# Same domain owwner

aws codeartifact copy-package-versions --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} \
  --source-repository ${ACCOUNT_3_TEAM_3_REPO} \
  --destination-repository ${ACCOUNT_1_SHARED_REPO_1} \
  --package dummyapp3 \
  --format pypi \
  --versions '["1.0.0"]' \
  --profile ${AWS_PROFILE_3}

# Test - check hash of the package in both ACCOUNT_1 and ACCOUNT_3

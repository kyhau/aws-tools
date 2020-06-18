#!/bin/bash
# Copy packages between repositories
# https://docs.aws.amazon.com/codeartifact/latest/ug/copy-package.html

source .config

aws codeartifact copy-package-versions --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} \
  --source-repository ${SHARED_REPO_1} \
  --destination-repository ${SHARED_REPO_2} \
  --package warrant --format pypi \
  --versions '["0.6.1"]'

#!/bin/bash
set -e

source .env

# Calling the update-repository command replaces the existing configured upstream repositories with
# the list of repositories provided with the --upstreams flag. If you want to add upstream repositories
# and keep the existing ones, you must include the existing upstream repositories in the call.

aws codeartifact update-repository --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} \
  --repository ${ACCOUNT_1_TEAM_1_REPO} \
  --upstreams \
    repositoryName=${ACCOUNT_1_SHARED_REPO_1} \
    repositoryName=external-npmjs \
    repositoryName=external-pypi \
  --profile ${AWS_PROFILE_1}

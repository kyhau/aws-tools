#!/bin/bash
set -e

source .env

aws codeartifact create-repository --domain ${DOMAIN} --domain-owner ${ACCOUNT_2_ID} \
  --repository ${ACCOUNT_2_TEAM_2_REPO} --description "Team repository" --profile ${AWS_PROFILE_2}

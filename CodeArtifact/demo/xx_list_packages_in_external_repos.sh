#!/bin/bash
source .env

declare -a REPOS=(
  "maven-central"
  "maven-clojars"
  "maven-commonsware"
  "maven-googleandroid"
  "maven-gradleplugins"
  "npmjs"
  "nuget-org"
  "pypi"
)

for repo_name in "${REPOS[@]}" ; do
  echo "CheckPt: account 1: list-packages external-${repo_name}"
  aws codeartifact list-packages --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} --repository external-${repo_name} --profile ${AWS_PROFILE_1}
done

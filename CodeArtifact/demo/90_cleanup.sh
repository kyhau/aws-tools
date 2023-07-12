#!/bin/bash
source .env

echo "CheckPt: Cleaning up account 3"

aws codeartifact delete-repository --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} \
  --repository ${ACCOUNT_3_TEAM_3_REPO} --profile ${AWS_PROFILE_3}


echo "CheckPt: Cleaning up account 2"

aws codeartifact delete-repository --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} \
  --repository ${ACCOUNT_2_TEAM_2_REPO} --profile ${AWS_PROFILE_2}


echo "CheckPt: Cleaning up account 1"

aws codeartifact delete-repository --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} \
  --repository ${ACCOUNT_1_SHARED_REPO_1} --profile ${AWS_PROFILE_1}

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

function delete_external() {
  EXTERNAL_REPO=${1}
  NEW_REPO="external-${1}"

  aws codeartifact delete-repository --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} \
    --repository ${NEW_REPO} --profile ${AWS_PROFILE_1}
}

for repo_name in "${REPOS[@]}" ; do
  delete_external ${repo_name}
done

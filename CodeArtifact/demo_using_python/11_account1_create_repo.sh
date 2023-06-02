#!/bin/bash
set -e

source .env

REPO=${ACCOUNT_1_TEAM_1_REPO}

aws codeartifact create-repository --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} \
  --repository ${REPO} --description "Team repository" --profile ${AWS_PROFILE_1}

# cd dist
# pip wheel yamllint
# npm pack cdk
# cd ..

# pip install -i https://pypi.org/simple twine

aws codeartifact login --tool twine --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} \
   --repository ${REPO} --profile ${AWS_PROFILE_1}

cat ~/.pypirc

twine upload --repository codeartifact dist/yamllint-1.32.0-py3-none-any.whl

aws codeartifact list-package-versions --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} \
  --repository ${REPO} --format pypi --package yamllint --profile ${AWS_PROFILE_1}

rm ~/.pypirc

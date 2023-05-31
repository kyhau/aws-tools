#!/bin/bash
set -e

source .env

# Download a wheel
# mkdir dist
# cd dist
# pip wheel boto3==1.20.35
# pip wheel cdk-monitoring-constructs==4.0.9
# cd ..

# pip install -i https://pypi.org/simple twine

REPO=${ACCOUNT_2_TEAM_2_REPO}

aws codeartifact login --tool twine --domain ${DOMAIN} --domain-owner ${ACCOUNT_2_ID} \
   --repository ${REPO} --profile ${AWS_PROFILE_2}

cat ~/.pypirc

# twine upload --repository codeartifact dist/boto3-1.20.35-py3-none-any.whl
twine upload --repository codeartifact dist/cdk_monitoring_constructs-4.0.9-py3-none-any.whl

aws codeartifact list-package-versions --domain ${DOMAIN} --domain-owner ${ACCOUNT_2_ID} \
  --repository ${REPO} --format pypi --package cdk-monitoring-constructs --profile ${AWS_PROFILE_2}

rm ~/.pypirc

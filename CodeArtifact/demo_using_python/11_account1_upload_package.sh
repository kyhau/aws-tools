#!/bin/bash
set -e

source .env

# Download a wheel
# mkdir dist
# cd dist
# pip wheel boto3==1.20.35
# cd ..

# pip install -i https://pypi.org/simple twine

aws codeartifact login --tool twine --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} \
   --repository ${ACCOUNT_1_SHARED_REPO_1} --profile ${AWS_PROFILE_1}
cat ~/.pypirc

twine upload --repository codeartifact dist/boto3-1.20.35-py3-none-any.whl

aws codeartifact list-package-versions --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} \
  --repository ${ACCOUNT_1_SHARED_REPO_1} --format pypi --package boto3 --profile ${AWS_PROFILE_1}

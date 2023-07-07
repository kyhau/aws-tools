#!/bin/bash
set -e

source .env

# Package a dummy wheel: see dummy-python-apps/package.sh

# pip install -i https://pypi.org/simple twine

PKG=dummy-python-apps/dist/dummyapp3-1.0.0-py2.py3-none-any.whl
REPO=${ACCOUNT_3_TEAM_3_REPO}
AWS_PROFILE=${AWS_PROFILE_3}

aws codeartifact login --tool twine --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} \
   --repository ${REPO} --profile ${AWS_PROFILE}

cat ~/.pypirc

twine upload --repository codeartifact ${PKG}

aws codeartifact list-package-versions --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} \
  --repository ${REPO} --format pypi --package dummyapp3 --profile ${AWS_PROFILE}

rm ~/.pypirc

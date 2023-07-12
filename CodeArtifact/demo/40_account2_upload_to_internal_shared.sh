#!/bin/bash
set -e

source .env

# Package a dummy wheel: see dummy-python-apps/package.sh

# pip install -i https://pypi.org/simple twine

PKG=dummy-python-apps/dist/dummyapp1-1.0.0-py2.py3-none-any.whl
REPO=${ACCOUNT_1_SHARED_REPO_1}
AWS_PROFILE=${AWS_PROFILE_1}

aws codeartifact login --tool twine --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} \
   --repository ${REPO} --profile ${AWS_PROFILE}

cat ~/.pypirc

twine upload --repository codeartifact ${PKG}

aws codeartifact list-package-versions --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} \
  --repository ${REPO} --format pypi --package dummyapp1 --profile ${AWS_PROFILE}

rm ~/.pypirc

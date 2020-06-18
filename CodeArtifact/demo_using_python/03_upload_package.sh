#!/bin/bash

source .config

# pip install -i https://pypi.org/simple twine

aws codeartifact login --tool twine --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} \
   --repository ${SHARED_REPO_1} --profile ${AWS_PROFILE_1}
cat ~/.pypirc

twine upload --repository codeartifact dist/warrant-0.6.1-py2.py3-none-any.whl

aws codeartifact list-package-versions --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} \
  --repository ${SHARED_REPO_1} --format pypi --package warrant

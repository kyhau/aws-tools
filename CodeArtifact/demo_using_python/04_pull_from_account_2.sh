#!/bin/bash

source .config

# Access a domain owned by an account you are authenticated to:

aws codeartifact list-package-versions --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} \
  --repository ${SHARED_REPO_1}  --format pypi --package warrant --profile ${AWS_PROFILE_2}

aws codeartifact login --tool pip --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} \
  --repository ${SHARED_REPO_1} --profile ${AWS_PROFILE_2}
cat ~/.config/pip/pip.conf

#pip install warrant

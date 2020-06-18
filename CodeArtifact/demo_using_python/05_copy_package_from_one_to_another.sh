#!/bin/bash
# Copy packages between repositories
# https://docs.aws.amazon.com/codeartifact/latest/ug/copy-package.html

source .config

aws codeartifact copy-package-versions --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} \
  --source-repository ${SHARED_REPO_1} \
  --destination-repository ${SHARED_REPO_2} \
  --package warrant --format pypi \
  --versions '["0.6.1"]'


# npm : A Node Package Manager (npm) package.
# pypi : A Python Package Index (PyPI) package.
# maven : A Maven package that contains compiled code in a distributable format, such as a JAR file.

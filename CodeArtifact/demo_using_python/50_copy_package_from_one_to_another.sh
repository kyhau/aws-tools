#!/bin/bash
# Copy packages between repositories
# https://docs.aws.amazon.com/codeartifact/latest/ug/copy-package.html

source .config

export REPO_1=team-2-dev  # owner == account 2
export REPO_2=team-2-prd  # owner == account 2
export REPO_3=team-2-shared-a  # owner == account 1

# Same domain owwner
aws codeartifact copy-package-versions --domain ${DOMAIN} --domain-owner ${ACCOUNT_2_ID} \
  --source-repository ${REPO_1} \
  --destination-repository ${REPO_2} \
  --package boto3 --format pypi \
  --versions '["1.20.35"]' \
  --profile ${AWS_PROFILE_2}

# Cannot copy if have diff domain owner
# Repos have Diff domain owners
# This will fail - An error occurred (ResourceNotFoundException) when calling the CopyPackageVersions operation:
# Repository not found. Repository 'team-2-dev' in domain '$DOMAIN' owned by account 'ACCOUNT_1_ID' does not exist.

aws codeartifact copy-package-versions --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} \
  --source-repository ${REPO_2} \
  --destination-repository ${REPO_3} \
  --package boto3 --format pypi \
  --versions '["1.20.35"]' \
  --profile ${AWS_PROFILE_2}


# npm : A Node Package Manager (npm) package.
# pypi : A Python Package Index (PyPI) package.
# maven : A Maven package that contains compiled code in a distributable format, such as a JAR file.

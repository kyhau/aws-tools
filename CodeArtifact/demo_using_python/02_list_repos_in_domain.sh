#!/bin/bash
# https://docs.aws.amazon.com/codeartifact/latest/ug/domain-overview.html
# https://docs.aws.amazon.com/codeartifact/latest/ug/list-repos.html

source .env

# List repositories in the domain

echo "Account 1: List repos from domain at account 1"
aws codeartifact list-repositories-in-domain --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} --profile ${AWS_PROFILE_1}

echo "Account 2: List repos from domain at account 1"
aws codeartifact list-repositories-in-domain --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} --profile ${AWS_PROFILE_2}

echo "Account 2: List repos from domain at account 2"
aws codeartifact list-repositories-in-domain --domain ${DOMAIN} --domain-owner ${ACCOUNT_2_ID} --profile ${AWS_PROFILE_2}

echo "Account 1: List repos from domain at account 2 (expect to fail)"
aws codeartifact list-repositories-in-domain --domain ${DOMAIN} --domain-owner ${ACCOUNT_2_ID} --profile ${AWS_PROFILE_1}


# administratorAccount - The AWS account ID that manages the repository.
# domainOwner - The 12-digit account number of the AWS account that owns the domain. It does not include dashes or spaces.

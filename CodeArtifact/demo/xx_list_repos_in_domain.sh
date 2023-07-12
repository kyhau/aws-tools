#!/bin/bash
# https://docs.aws.amazon.com/codeartifact/latest/ug/domain-overview.html
# https://docs.aws.amazon.com/codeartifact/latest/ug/list-repos.html

source .env

# List repositories in the domain

echo "CheckPt: account 1: List repos"
aws codeartifact list-repositories-in-domain --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} --profile ${AWS_PROFILE_1}

echo "CheckPt: account 2: List repos"
aws codeartifact list-repositories-in-domain --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} --profile ${AWS_PROFILE_2}

echo "CheckPt: account 3: List repos"
aws codeartifact list-repositories-in-domain --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} --profile ${AWS_PROFILE_3}

# administratorAccount - The AWS account ID that manages the repository.
# domainOwner - The 12-digit account number of the AWS account that owns the domain. It does not include dashes or spaces.

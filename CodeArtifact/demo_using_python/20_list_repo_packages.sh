#!/bin/bash
# https://docs.aws.amazon.com/codeartifact/latest/ug/domain-overview.html
# https://docs.aws.amazon.com/codeartifact/latest/ug/list-repos.html

source .config

# Access a domain owned by an account you are authenticated to:

aws codeartifact list-packages --domain ${DOMAIN} --repository ${ACCOUNT_1_SHARED_REPO_1} --profile ${AWS_PROFILE_1}
aws codeartifact list-packages --domain ${DOMAIN} --repository ${ACCOUNT_1_SHARED_REPO_2} --profile ${AWS_PROFILE_1}


# Access a domain owned by an account you are authenticated to:

aws codeartifact list-packages --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} --repository ${ACCOUNT_1_SHARED_REPO_1} --profile ${AWS_PROFILE_2}
aws codeartifact list-packages --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} --repository ${ACCOUNT_1_SHARED_REPO_1} --profile ${AWS_PROFILE_2}


# List repositories in the domain

aws codeartifact list-repositories-in-domain --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} --profile ${AWS_PROFILE_1}
aws codeartifact list-repositories-in-domain --domain ${DOMAIN} --domain-owner ${ACCOUNT_2_ID} --profile ${AWS_PROFILE_2}

# administratorAccount - The AWS account ID that manages the repository.
# domainOwner - The 12-digit account number of the AWS account that owns the domain. It does not include dashes or spaces.

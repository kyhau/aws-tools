#!/bin/bash
# https://docs.aws.amazon.com/codeartifact/latest/ug/domain-overview.html

source .config

# Access a domain owned by an account you are authenticated to:

aws codeartifact list-packages --domain ${DOMAIN} --repository ${SHARED_REPO_1} --profile ${AWS_PROFILE_1}
aws codeartifact list-packages --domain ${DOMAIN} --repository ${SHARED_REPO_2} --profile ${AWS_PROFILE_1}


# Access a domain owned by an account you are authenticated to:

aws codeartifact list-packages --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} --repository ${SHARED_REPO_1} --profile ${AWS_PROFILE_2}
aws codeartifact list-packages --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} --repository ${SHARED_REPO_2} --profile ${AWS_PROFILE_2}

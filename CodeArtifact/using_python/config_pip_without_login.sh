#!/bin/bash
# Configure pip without the login command
# https://docs.aws.amazon.com/codeartifact/latest/ug/python-configure-without-pip.html

ACCOUNT_ID="TODO"
DOMAIN="TODO"
REPO="TODO"

# If you cannot use the login command to configure pip, you can use pip config.
# 1.  Use the AWS CLI to fetch a new authorization token.
#     Note: If you are accessing a repository in a domain that you own, you do not need to include the --domain-owner.

CODEARTIFACT_TOKEN=$(aws codeartifact get-authorization-token --domain ${DOMAIN} --domain-owner ${ACCOUNT_ID})

cat ${CODEARTIFACT_TOKEN}

# 2. Use pip config to set the CodeArtifact registry URL and credentials.
#    The registry URL must end with a forward slash (/). Otherwise, you cannot connect to the repository.

pip config set global.index-url https://aws:${CODEARTIFACT_TOKEN}@${DOMAIN}.d.codeartifact.ap-southeast-2.amazonaws.com/pypi/${REPO}/simple/

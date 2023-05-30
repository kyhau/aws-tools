#!/bin/bash
set -e
# https://docs.aws.amazon.com/codeartifact/latest/ug/domains.html

source .env

# Domain names only need to be unique within an account

aws codeartifact create-domain --domain ${DOMAIN} --profile ${AWS_PROFILE_1}

aws codeartifact list-domains --profile ${AWS_PROFILE_1}

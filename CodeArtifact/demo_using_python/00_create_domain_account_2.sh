#!/bin/bash
# https://docs.aws.amazon.com/codeartifact/latest/ug/domains.html

source .config

# Domain names only need to be unique within an account

aws codeartifact create-domain --domain ${DOMAIN} --profile ${AWS_PROFILE_2}

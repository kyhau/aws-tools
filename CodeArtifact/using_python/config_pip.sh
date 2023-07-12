#!/bin/bash
# Configure clients with the login command
# https://docs.aws.amazon.com/codeartifact/latest/ug/python-configure.html

ACCOUNT_ID="TODO"
DOMAIN="TODO"
REPO="TODO"

aws codeartifact login --tool pip --repository $REPO --domain $DOMAIN --domain-owner $ACCOUNT_ID

# Configure pip for use with CodeArtifact by editing ~/.config/pip/pip.conf to set the index-url to the repository specified by the --repository option.
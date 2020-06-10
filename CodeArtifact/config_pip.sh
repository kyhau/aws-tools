#!/bin/bash

ACCOUNT_ID="TODO"
DOMAIN="TODO"
REPO="TODO"

aws codeartifact login --tool pip --repository $REPO --domain $DOMAIN --domain-owner $ACCOUNT_ID

#aws codeartifact list-packages --domain my-example-domain --repository npm-pypi-example-repository

#!/bin/bash
set -e
# See https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install-linux.html

brew upgrade aws-sam-cli

sam --version

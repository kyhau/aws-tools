#!/bin/bash
set -e
# See https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install-linux.html

# Note: This installation will cause your environment's default Python version to be the one installed by Homebrew.

brew tap aws/tap
brew install aws-sam-cli

# To upgrade:
# brew upgrade aws/tap/aws-sam-cli

sam --version

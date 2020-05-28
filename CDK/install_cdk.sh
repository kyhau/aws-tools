#!/bin/bash
# https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html
set -e

# Prerequisites
# - Node.js (>= 10.3.0)
echo "node version: $(node --version)"
echo "npm version: $(npm --version)"

#echo "Uninstalling the AWS CDK.
#sudo npm uninstall -g aws-cdk

#npm config set registry http://registry.npmjs.org/

echo "Installing the AWS CDK..."
sudo npm install -g aws-cdk
echo "cdk version: $(cdk --version)"

# Updating Your Language (Python) Dependencies
#pip install --upgrade aws-cdk.core

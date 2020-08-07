#!/bin/bash
# https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html
set -e

# Prerequisites
# - Node.js (>= 10.3.0)

npm cache clear --force

sudo apt-get install -y nodejs
echo "node version: $(node --version)"
echo "npm version: $(npm --version)"

# Optional: useful for cdk-patterns/serverless
#npm config set registry http://registry.npmjs.org/
#sudo npm uninstall -g npx
sudo npm install -g npx --force
echo "npx version: $(npx --version)"

#echo "Uninstalling the AWS CDK.
#sudo npm uninstall -g aws-cdk

echo "Installing the AWS CDK..."
sudo npm install -g aws-cdk
echo "cdk version: $(cdk --version)"

# Updating Your Language (Python) Dependencies
pip install -U aws-cdk.core

#!/bin/bash
# https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html
set -e

# Prerequisites
# - Node.js (>= 10.3.0)

npm cache clear --force

sudo apt-get install -y nodejs
echo "node version: $(node --version)"
echo "npm version: $(npm --version)"

#echo "Uninstalling the AWS CDK.
#sudo npm uninstall -g aws-cdk

# If seeing enoent ENOENT: no such file or directory, chmod '/usr/lib/node_modules/aws-cdk/bin/cdk'
#sudo rm -rf /usr/lib/node_modules/aws-cdk/

echo "Installing the AWS CDK..."
sudo npm install -g aws-cdk@next
echo "cdk version: $(cdk --version)"

# Updating Your Language (Python) Dependencies
pip install -U aws-cdk-lib constructs

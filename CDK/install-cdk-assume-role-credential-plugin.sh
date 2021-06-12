#!/bin/bash
# https://github.com/aws-samples/cdk-assume-role-credential-plugin
set -e

npm cache clear --force

sudo apt-get install -y nodejs
echo "node version: $(node --version)"
echo "npm version: $(npm --version)"

echo "Installing the plugin globally..."
sudo npm install -g cdk-assume-role-credential-plugin
echo "cdk-assume-role-credential-plugin version: $(cdk-assume-role-credential-plugin --version)"

# OR install it locally...
# npm install cdk-assume-role-credential-plugin

#!/bin/bash
# https://github.com/aws-samples/cdk-assume-role-credential-plugin
set -e

git clone git@github.com:aws-samples/cdk-assume-role-credential-plugin.git

cd cdk-assume-role-credential-plugin
echo "Install the plugin globally..."

npm install -g git+https://github.com/aws-samples/cdk-assume-role-credential-plugin.git

# OR install it locally...
# npm install git+https://github.com/aws-samples/cdk-assume-role-credential-plugin.git

cd ..

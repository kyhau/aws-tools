#!/bin/bash
# https://github.com/awslabs/cdk8s

# Prerequisites
# - Node.js (>= 8.11.x)
echo "npm version: $(npm --version)"

#echo "Uninstalling the AWS CDK..."
#sudo npm uninstall -g aws-cdk

#npm config set registry http://registry.npmjs.org/

echo "Installing the AWS cdk8s..."
sudo npm install -g cdk8s-cli
echo "cdk8s version: $(cdk8s --version)"

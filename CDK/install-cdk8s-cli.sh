#!/bin/bash
# https://github.com/cdk8s-team/cdk8s-cli
set -e

# Prerequisites
# - Node.js (>= 10.3.0)

npm cache clear --force

sudo apt-get install -y nodejs
echo "INFO: node version: $(node --version)"
echo "INFO: npm version: $(npm --version)"

#echo "INFO: Uninstalling cdk8s-cli"
#sudo npm uninstall -g cdk8s-cli

echo "INFO: Installing cdk8s-cli"
sudo npm i -g cdk8s-cli
echo "INFO: cdk8s version: $(cdk8s --version)"


#!/bin/bash
# https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html
set -e

# Prerequisites
# - Node.js (>= 10.3.0)
#npm cache clear --force
#sudo apt-get install -y nodejs

echo "INFO: cdk version: $(cdk --version)"
echo "INFO: node version: $(node --version)"
echo "INFO: npm version: $(npm --version)"

#echo "INFO: Uninstalling CDK"
#sudo npm uninstall -g aws-cdk

# If seeing enoent ENOENT: no such file or directory, chmod '/usr/lib/node_modules/aws-cdk/bin/cdk'
#sudo rm -rf /usr/lib/node_modules/aws-cdk/

echo "INFO: Installing CDK"
#sudo npm install -g aws-cdk@next
sudo npm install -g aws-cdk
echo "INFO: cdk version: $(cdk --version)"

# Updating Your Language (Python) Dependencies
echo "INFO: TODO for python: pip install -U aws-cdk-lib constructs"

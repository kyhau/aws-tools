#!/bin/bash
# https://github.com/cdklabs/cdk-import
set -e

echo "INFO: Installing cdk-import"
sudo npm install -g cdk-import
echo "INFO: cdk-import version: $(cdk-import --version)"

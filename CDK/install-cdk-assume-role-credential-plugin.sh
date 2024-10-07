#!/bin/bash
# https://github.com/aws-samples/cdk-assume-role-credential-plugin
set -e

_SUDO=
[[ "$(uname)" = "Darwin" ]] || _SUDO=sudo  # If it is not macOS, _SUDO will be set to sudo

npm cache clear --force

$_SUDO apt-get install -y nodejs
echo "INFO: node version: $(node --version)"
echo "INFO: npm version: $(npm --version)"

echo "INFO: Installing the plugin globally"
$_SUDO npm install -g cdk-assume-role-credential-plugin
echo "INFO: cdk-assume-role-credential-plugin version: $(cdk-assume-role-credential-plugin --version)"

# OR install it locally...
# npm install cdk-assume-role-credential-plugin

#!/bin/bash
# https://github.com/cdklabs/cdk-import
set -e

_SUDO=
[[ "$(uname)" = "Darwin" ]] || _SUDO=sudo  # If it is not macOS, _SUDO will be set to sudo

echo "INFO: Installing cdk-import"
$_SUDO npm install -g cdk-import
echo "INFO: cdk-import version: $(cdk-import --version)"

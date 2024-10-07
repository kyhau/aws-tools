#!/bin/bash
https://github.com/cdk-patterns/serverless
set -e

_SUDO=
[[ "$(uname)" = "Darwin" ]] || _SUDO=sudo  # If it is not macOS, _SUDO will be set to sudo

#npm config set registry http://registry.npmjs.org/
#sudo npm uninstall -g npx
$_SUDO npm install -g npx --force
echo "INFO: npx version: $(npx --version)"

npx cdkp list

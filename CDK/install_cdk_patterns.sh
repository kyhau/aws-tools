#!/bin/bash
https://github.com/cdk-patterns/serverless
set -e

#npm config set registry http://registry.npmjs.org/
#sudo npm uninstall -g npx
sudo npm install -g npx --force
echo "npx version: $(npx --version)"

npx cdkp list

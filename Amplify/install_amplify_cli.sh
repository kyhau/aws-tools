#!/bin/bash
# https://docs.amplify.aws/cli/start/install
set -e

# Prerequisites
# - Node.js (>= 10.x) and npm (>- 6.x)
npm cache clear --force

sudo apt-get install -y nodejs
echo "node version: $(node --version)"
echo "npm version: $(npm --version)"

sudo npm install -g @aws-amplify/cli

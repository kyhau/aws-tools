#!/bin/bash
set -e
# Ref: https://github.com/aws-cloudformation/cloudformation-guard

echo "Installing Pre-Built Release Binaries"

REPO_NAME="aws-cloudformation/cloudformation-guard"
VERSION=$(curl --silent "https://api.github.com/repos/${REPO_NAME}/releases/latest" --insecure -s | grep -Po '"tag_name": "\K.*.*?(?=")')
ZIP_FILE="https://github.com/${REPO_NAME}/releases/download/${VERSION}/cfn-guard-v2-ubuntu-latest.tar.gz"

echo "Downloading the latest version..."
wget ${ZIP_FILE}
tar -xvf cfn-guard-v2-ubuntu-latest.tar.gz

echo "Coping binary to .local/bin..."
mkdir -p ~/.local/bin
DEST=~/.local/bin/cfn-guard
[[ -e "$DEST" ]] && rm -f ${DEST}
mv cfn-guard-v2-ubuntu-latest/cfn-guard ${DEST}

rm -rf cfn-guard-v2-ubuntu-latest.tar.gz cfn-guard-v2-ubuntu-latest

echo "Version installed:"
cfn-guard --version

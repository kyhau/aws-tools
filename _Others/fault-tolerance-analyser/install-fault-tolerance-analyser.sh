#!/bin/bash
# Set to fail script if any command fails.
set -e

INSTALL_DIR="$HOME/workspaces/github"
ori_dir=$(pwd)

cd $INSTALL_DIR

if [[ ! -d "fault-tolerance-analyser" ]]; then
  git clone https://github.com/aws-samples/fault-tolerance-analyser
fi

cd fault-tolerance-analyser
git pull

cd ${ori_dir}

echo "TODO: pip install -r requirements.txt"

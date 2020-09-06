#!/bin/bash
# Install https://github.com/kyhau/aws-tools

set -e
# TODO: Create and activate virtualenv for not installing in global python environment

SRC_HOME="$( cd "$( dirname -- "$0" )" && pwd )/aws-tools"

if [[ -d "${SRC_HOME}/aws-tools" ]]; then
  echo "$SRC_HOME already exists"
else
  echo "Cloning kyhau/aws-tools to $SRC_HOME"
  git clone git@github.com:kyhau/aws-tools.git
fi

pushd aws-tools
pip install -r requirements.txt

source .aliases
popd

cat "[[ ! -f "${SRC_HOME}/.aliases" ]] || . ${SRC_HOME}/.aliases" >> ~/.bashrc

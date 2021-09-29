#!/bin/bash
# kubectx + kubens: Power tools for kubectl
# https://github.com/ahmetb/kubectx

set -e

mkdir -p .local/bin

if [[ -d "~/.local/kubectx" ]]
then
  cd ~/.local/kubectx
  git pull
  cd -
else
  git clone git@github.com:ahmetb/kubectx.git ~/.local/kubectx
  ln -s ~/.local/kubectx/kubectx ~/.local/bin/kubectx
  ln -s ~/.local/kubectx/kubens ~/.local/bin/kubens
fi

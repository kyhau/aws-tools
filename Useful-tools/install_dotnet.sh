#!/bin/bash
set -e

# See https://docs.microsoft.com/en-us/dotnet/core/tools/dotnet-install-script

echo "Downloading dotnet-install.sh ..."
wget https://dot.net/v1/dotnet-install.sh -o /tmp/dotnet-install.sh
chmod +x /tmp/dotnet-install.sh --runtime dotnet
. /tmp/dotnet-install.sh

echo "export DOTNET_ROOT=$HOME/.dotnet" >> $HOME/.bash_profile
echo "export PATH=$PATH:$HOME/.dotnet" >> $HOME/.bash_profile
source ~/.bash_profile

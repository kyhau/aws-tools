#!/bin/bash
# https://github.com/elpy1/ssh-over-ssm

set -e

INSTALL_DIR="$HOME/workspaces/github"
ORI_DIR=$(pwd)

cd $INSTALL_DIR

if [[ ! -d "ssh-over-ssm" ]]; then
  git clone https://github.com/elpy1/ssh-over-ssm
else
  cd ssh-over-ssm
  git pull
fi

cd ${ORI_DIR}

echo """
NOTE: Make sure your SSH config (~/.ssh/config) include
==========================================================================
# applies to all hosts and ensures our SSH sessions remain alive when idle
Host *
  TCPKeepAlive yes
  ServerAliveInterval 30
  ConnectTimeout 10

#------
# place any other/existing configuration here
#------

Match Host i-*
  ProxyCommand ssh-ssm.sh %h %r
  IdentityFile ~/.ssh/ssm-ssh-tmp
  StrictHostKeyChecking no
  BatchMode yes
---
"""

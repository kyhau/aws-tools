#!/bin/bash
# Set to fail script if any command fails.
set -e

INSTALL_DIR="$HOME/workspaces/github"

ori_dir=$(pwd)

cd $INSTALL_DIR

if [[ ! -d "git-secrets" ]]; then
  git clone https://github.com/awslabs/git-secrets
fi

cd git-secrets
git pull
sudo make install

cd ${ori_dir}

# Add a configuration template if you want to add hooks to all repositories you initialize or clone in the future.
git secrets --register-aws --global

# Add hooks to all your local repositories.
git secrets --install ~/.git-templates/git-secrets
git config --global init.templateDir ~/.git-templates/git-secrets

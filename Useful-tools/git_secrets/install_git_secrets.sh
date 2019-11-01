#!/bin/bash
# Set to fail script if any command fails.
set -e

WORKSPACE_DIR="$HOME/workspaces/github"

pushd $WORKSPACE_DIR

[[ ! -d "$REPO_DIR" ]] || git clone https://github.com/awslabs/git-secrets

pushd git-secrets
sudo make install

popd
popd

# Add a configuration template if you want to add hooks to all repositories you initialize or clone in the future.
git secrets --register-aws --global

# Add hooks to all your local repositories.
git secrets --install ~/.git-templates/git-secrets
git config --global init.templateDir ~/.git-templates/git-secrets

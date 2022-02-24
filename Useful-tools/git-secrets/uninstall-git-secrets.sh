#!/bin/bash
# Set to fail script if any command fails.
set -e

find . -regex '.*/\.git/hooks/commit-msg' -exec sed -i '' -e 's/git secrets --commit_msg_hook -- "$@"//' {} \;
find . -regex '.*/\.git/hooks/pre-commit' -exec sed -i '' -e 's/git secrets --pre_commit_hook -- "$@"//' {} \;
find . -regex '.*/\.git/hooks/prepare-commit-msg' -exec sed -i '' -e 's/git secrets --prepare_commit_msg_hook -- "$@"//' {} \;

cd ~/.git-templates
rm -rf git-secrets
cd -

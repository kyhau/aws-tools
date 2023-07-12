#!/bin/bash
# AWS CloudShell compute environment: specifications and software https://docs.aws.amazon.com/cloudshell/latest/userguide/vm-specs.html

echo "Inspect compute environment"

echo "--------------------------------------------------------------------------------"
echo "Pre-installed shells"
bash --version 2>&1 | head -n 1
zsh --version
echo "--------------------------------------------------------------------------------"

echo "AWS CLI"
aws --version
eb --version
ecs-cli --version
sam --version
echo "--------------------------------------------------------------------------------"

echo "Runtimes and AWS SDKs"
echo "node $(node --version)"
echo "npm $(npm --version)"
npm -g ls --depth 0 2>/dev/null | grep aws-sdk | awk -F ' ' '{ print $2}'
python --version
python3 --version
pip3 --version
pip3 freeze | grep boto3
echo "--------------------------------------------------------------------------------"

echo "Development tools and shell utilities"
pip3 freeze | grep git-remote-codecommit
git --version
jq --version

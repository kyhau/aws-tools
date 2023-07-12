#!/bin/bash
set -e
# See https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install-linux.html

# AWS SAM Accelerate
# To use the AWS SAM Accelerate, you must install version 1.34.1 or greater of the AWS SAM CLI
# https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/accelerate-getting-started.html

echo "INFO: Downloading aws-sam-cli"
wget https://github.com/aws/aws-sam-cli/releases/latest/download/aws-sam-cli-linux-x86_64.zip

# Verify the integrity and authenticity of the downloaded installer files by generating a hash value using the following command:
sha256sum aws-sam-cli-linux-x86_64.zip

# Unzip the installation files into the sam-installation/ subdirectory.
unzip aws-sam-cli-linux-x86_64.zip -d sam-installation

if [[ -d "/usr/local/aws-sam-cli/current" ]]
then
  echo "INFO: Updating sam"
  sudo ./sam-installation/install --update
else
  echo "INFO: Installing sam"
  sudo ./sam-installation/install
fi

echo "INFO: Checking version"
echo "sam version: $(sam --version)"

rm -rf sam-installation
rm aws-sam-cli-linux-x86_64.zip

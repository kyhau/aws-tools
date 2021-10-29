#!/bin/bash
set -e
# See https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-cdk-getting-started.html
# See https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install-linux.html

echo "INFO: Downloading sam-cli-beta-cdk"
wget https://github.com/aws/aws-sam-cli/releases/download/sam-cli-beta-cdk/aws-sam-cli-linux-x86_64.zip

# Verify the integrity and authenticity of the downloaded installer files by generating a hash value using the following command:
sha256sum aws-sam-cli-linux-x86_64.zip

# Unzip the installation files into the sam-installation/ subdirectory.
unzip aws-sam-cli-linux-x86_64.zip -d sam-installation

if [[ -d "/usr/local/aws-sam-cli-beta-cdk/current" ]]
then
  echo "INFO: Updating sam-beta-cdk"
  sudo ./sam-installation/install --update
else
  echo "INFO: Installing sam-beta-cdk"
  sudo ./sam-installation/install
fi

echo "INFO: Checking version"
echo "sam-beta-cdk version: $(sam-beta-cdk --version)"

rm -rf sam-installation
rm aws-sam-cli-linux-x86_64.zip

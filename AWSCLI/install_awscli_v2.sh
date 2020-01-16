#!/bin/bash
set -e

# See https://aws.amazon.com/blogs/developer/aws-cli-v2-installers/
# See https://aws.amazon.com/blogs/developer/aws-cli-v2-now-supports-aws-single-sign-on/

curl 'https://d1vvhvl2y92vvt.cloudfront.net/awscli-exe-linux-x86_64.zip' -o 'awscli-exe.zip'

unzip awscli-exe.zip

[[ -e "/usr/local/aws-cli/v2/current" ]] && sudo rm /usr/local/aws-cli/v2/current

# Install the AWS CLI v2 preview under the /usr/local/aws-cli and create an aws2 symlink in /usr/local/bin
sudo ./aws/install

rm -rf awscli-exe.zip ./aws

aws2 --version

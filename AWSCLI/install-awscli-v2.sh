#!/bin/bash
set -e
# See https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-linux.html#cliv2-linux-install
# See https://aws.amazon.com/blogs/developer/aws-cli-v2-now-supports-aws-single-sign-on/

echo "INFO: Downloading awscliv2"
cd /tmp
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip

echo "INFO: Installing binary to ~/.local/bin"
mkdir -p ~/.local/bin

rm ~/.local/bin/aws || true
rm -rf ~/.local/aws-cli || true

./aws/install --install-dir ~/.local/aws-cli --bin-dir ~/.local/bin

echo "INFO: Checking version"
echo "aws version: $(aws --version)"

rm -rf /tmp/awscliv2.zip /tmp/aws
cd -

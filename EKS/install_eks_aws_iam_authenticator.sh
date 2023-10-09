#!/bin/bash
# Install Amazon EKS aws-iam-authenticator
# https://github.com/kubernetes-sigs/aws-iam-authenticator/releases

set -e

if [ -x "$(command -v aws-iam-authenticator)" ]; then
  echo "INFO: aws-iam-authenticator version: $(aws-iam-authenticator version)"
else
  echo "INFO: aws-iam-authenticator not installed"
fi

VERSION=$(curl -Ls https://github.com/kubernetes-sigs/aws-iam-authenticator/releases/latest | grep 'href="/kubernetes-sigs/aws-iam-authenticator/releases/tag' | awk -F ' ' '{print $NF}' | cut -c 2-)

echo "INFO: Downloading aws-iam-authenticator binary from Amazon S3"
curl -L -o aws-iam-authenticator https://github.com/kubernetes-sigs/aws-iam-authenticator/releases/download/v${VERSION}/aws-iam-authenticator_${VERSION}_linux_amd64
chmod +x ./aws-iam-authenticator

echo "INFO: Coping binary to ~/.local/bin"
mkdir -p ~/.local/bin
# rm ~/.local/bin/aws-iam-authenticator || true
mv aws-iam-authenticator ~/.local/bin/

echo "INFO: aws-iam-authenticator version: $(aws-iam-authenticator version)"

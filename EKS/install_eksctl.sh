#!/bin/bash
# Install the official Amazon EKS command line utility for creating and managing Kubernetes clusters on Amazon EKS
# https://docs.aws.amazon.com/eks/latest/userguide/eksctl.html

set -e

if [ -x "$(command -v eksctl)" ]; then
  echo "INFO: eksctl version: $(eksctl version)"
else
  echo "INFO: eksctl not installed"
fi

echo "INFO: Downloading eksctl"
curl -s --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C .

echo "INFO: Moving binary to ~/.local/bin"
mkdir -p ~/.local/bin
mv eksctl ~/.local/bin/

echo "INFO: eksctl version: $(eksctl version)"

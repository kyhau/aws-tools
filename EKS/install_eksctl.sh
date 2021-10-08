#!/bin/bash
# Install the official Amazon EKS command line utility for creating and managing Kubernetes clusters on Amazon EKS
# https://docs.aws.amazon.com/eks/latest/userguide/eksctl.html

set -e

echo "INFO: Downloading eksctl"
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C .

echo "INFO: Moving binary to ~/.local/bin"
mkdir -p ~/.local/bin
mv eksctl ~/.local/bin/

echo "INFO: Checking version"
echo "eksctl version: $(eksctl version)"

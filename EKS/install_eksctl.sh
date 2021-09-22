#!/bin/bash
# Install the official Amazon EKS command line utility for creating and managing Kubernetes clusters on Amazon EKS
# https://docs.aws.amazon.com/eks/latest/userguide/eksctl.html

set -e

echo "Downloading the latest version of eksctl..."
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp

echo "Moving the extracted binary to ~/.local/bin..."
mkdir -p ~/.local/bin
mv /tmp/eksctl ~/.local/bin/

echo "Checking version..."
echo "eksctl version: $(eksctl version)"

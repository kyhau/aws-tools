#!/bin/bash
# https://kubectl.docs.kubernetes.io/installation/kustomize/binaries/

set -e

echo "Downloading the latest version of kustomize..."
curl -s "https://raw.githubusercontent.com/kubernetes-sigs/kustomize/master/hack/install_kustomize.sh"  | bash

echo "Moving the extracted binary to ~/.local/bin..."
mkdir -p ~/.local/bin
mv kustomize ~/.local/bin/

echo "Checking version..."
echo "kustomize version: $(kustomize version)"

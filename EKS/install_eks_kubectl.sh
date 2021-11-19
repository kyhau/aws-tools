#!/bin/bash
# Install Amazon EKS-vended kubectl, the Kubernetes command line utility for communicating with the cluster API server.
# https://docs.aws.amazon.com/eks/latest/userguide/install-kubectl.html
# https://github.com/kubernetes/kubectl

set -e

VERSION=1.21.2
REL_DATE=2021-07-05

echo "Downloading the Amazon EKS-vended kubectl binary for your cluster's Kubernetes version from Amazon S3..."
pushd ~
curl -o kubectl "https://amazon-eks.s3-us-west-2.amazonaws.com/${VERSION}/${REL_DATE}/bin/linux/amd64/kubectl"

chmod +x ./kubectl

echo "Coping binary to ~/.local/bin and create a symlink for bookmarking the version..."
mkdir -p ~/.local/bin
rm ~/.local/bin/kubectl || true
rm ~/.local/bin/kubectl-v${VERSION} || true

mv kubectl ~/.local/bin/
pushd ~/.local/bin
ln -s kubectl kubectl-v${VERSION}
popd

popd

echo "Checking version..."
kubectl version --short --client

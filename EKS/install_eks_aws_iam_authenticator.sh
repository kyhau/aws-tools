#!/bin/bash
# Install Amazon EKS-vended aws-iam-authenticator
# https://docs.aws.amazon.com/eks/latest/userguide/install-aws-iam-authenticator.html

set -e

VERSION=1.21.2
REL_DATE=2021-07-05

echo "Downloading the Amazon EKS-vended aws-iam-authenticator binary from Amazon S3..."
pushd ~
curl -o aws-iam-authenticator "https://amazon-eks.s3-us-west-2.amazonaws.com/${VERSION}/${REL_DATE}/bin/linux/amd64/aws-iam-authenticator"

chmod +x ./aws-iam-authenticator

echo "Coping binary to ~/.local/bin and create a symlink for bookmarking the version..."
mkdir -p ~/.local/bin
rm ~/.local/bin/aws-iam-authenticator || true
rm ~/.local/bin/aws-iam-authenticator-v${VERSION} || true

mv aws-iam-authenticator ~/.local/bin/
pushd ~/.local/bin
ln -s aws-iam-authenticator aws-iam-authenticator-v${VERSION}
popd

popd

echo "Checking version..."
aws-iam-authenticator version

echo "Try aws-iam-authenticator help"

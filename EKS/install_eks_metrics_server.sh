#!/bin/bash
# Install the the Kubernetes Metrics Server
# https://docs.aws.amazon.com/eks/latest/userguide/metrics-server.html

set -e

VERSION=0.3.6

#mkdir -p /opt/kms/metrics-server
#pushd /opt/kms/metrics-server

echo "Downloading metrics-server ${VERSION}..."
curl -o "v${VERSION}.tar.gz" "https://github.com/kubernetes-incubator/metrics-server/archive/v${VERSION}.tar.gz"
tar -xvzf "v${VERSION}.tar.gz"

#tar -xzf metrics-server-$VERSION.tar.gz --directory "metrics-server-v${VERSION}" --strip-components 1

#kubectl apply -f metrics-server-$DOWNLOAD_VERSION/deploy/1.8+/

#popd

#echo "Checking metrics-server deployment is running the desired number of pods..."
#kubectl get deployment metrics-server -n kube-system

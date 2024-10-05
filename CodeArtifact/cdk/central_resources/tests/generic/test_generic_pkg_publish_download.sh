#!/bin/bash
set -e

echo "######################################################################"
echo "CheckPt: Install tools"

pip3 install -i https://pypi.org/simple -U awscli

echo "######################################################################"
echo "CheckPt: Package a dummy tar.gz package"

export PKG_NAME="dummyasset$(date +%Y%m%d%H%M%S)"
./package_dummy_targz.sh

PKG=${PKG_NAME}.tar.gz
PKG_NS=unittest

echo "######################################################################"
echo "CheckPt: Test publish"

export ASSET_SHA256=$(sha256sum ${PKG} | awk '{print $1;}')

# Generic packages must have a namespace
aws codeartifact publish-package-version --domain ${DOMAIN_NAME} --domain-owner ${DOMAIN_OWNER} \
  --repository ${TARGET_REPO_NAME} \
  --format generic --namespace ${PKG_NS} --package ${PKG_NAME} \
  --package-version "1.0.0" \
  --asset-content ${PKG} --asset-name ${PKG} \
  --asset-sha256 $ASSET_SHA256 \
  --region ${AWS_REGION}

echo "######################################################################"
echo "CheckPt: Test list-package-versions"

aws codeartifact list-package-versions --domain ${DOMAIN_NAME} --domain-owner ${DOMAIN_OWNER} \
  --repository ${TARGET_REPO_NAME} \
  --format generic --namespace ${PKG_NS} --package ${PKG_NAME} \
  --region ${AWS_REGION}

echo "######################################################################"
echo "CheckPt: Test download generic package assets ${PKG_NAME}"

aws codeartifact get-package-version-asset --domain ${DOMAIN_NAME} --domain-owner ${DOMAIN_OWNER} \
  --repository ${TARGET_REPO_NAME} \
  --format generic --namespace ${PKG_NS} --package ${PKG_NAME} \
  --package-version "1.0.0" \
  --asset ${PKG} \
  ${PKG} \
  --region ${AWS_REGION}

tar -xvf ${PKG}
rm ${PKG} app.sh

echo "######################################################################"
echo "CheckPt: Test delete package"

aws codeartifact delete-package --domain ${DOMAIN_NAME} --domain-owner ${DOMAIN_OWNER} \
  --repository ${TARGET_REPO_NAME} \
  --format generic --namespace ${PKG_NS} --package ${PKG_NAME} \
  --region ${AWS_REGION}

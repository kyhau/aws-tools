#!/bin/bash
set -e

echo "######################################################################"
echo "CheckPt: Install tools"

pip3 install -i https://pypi.org/simple -U awscli twine

echo "######################################################################"
echo "CheckPt: Package a dummy wheel"

export PKG_NAME="dummypythonapp$(date +%Y%m%d%H%M%S)"
PKG=dist/${PKG_NAME}-1.0.0-py2.py3-none-any.whl
./package_dummy_whl.sh

echo "######################################################################"
echo "CheckPt: Test publish"

aws codeartifact login --tool twine --domain ${DOMAIN_NAME} --domain-owner ${DOMAIN_OWNER} \
   --repository ${TARGET_REPO_NAME} --region ${AWS_REGION}

twine upload --repository codeartifact ${PKG} --verbose

rm ~/.pypirc
rm -rf dist/

echo "######################################################################"
echo "CheckPt: Test list-package-versions"

aws codeartifact list-package-versions --domain ${DOMAIN_NAME} --domain-owner ${DOMAIN_OWNER} \
  --repository ${TARGET_REPO_NAME} --format pypi --package ${PKG_NAME} --region ${AWS_REGION}

echo "######################################################################"
echo "CheckPt: Test pip3 install ${PKG_NAME}"

aws codeartifact login --tool pip --domain ${DOMAIN_NAME} --domain-owner ${DOMAIN_OWNER} \
  --repository ${TARGET_REPO_NAME} --region ${AWS_REGION}

pip3 install ${PKG_NAME}

rm ~/.config/pip/pip.conf

echo "######################################################################"
echo "CheckPt: Test delete package"

aws codeartifact delete-package --domain ${DOMAIN_NAME} --domain-owner ${DOMAIN_OWNER} \
  --repository ${TARGET_REPO_NAME} --format pypi --package ${PKG_NAME} --region ${AWS_REGION}

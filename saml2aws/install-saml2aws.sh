#!/bin/bash
set -e

VERSION=$(curl -s "https://api.github.com/repos/Versent/saml2aws/releases/latest" --insecure | grep -Po '"tag_name": "\K.*?(?=")' | sed 's/^v//')
echo "INFO: saml2aws latest: ${VERSION}"

CURR_VERSION=
if [ -x "$(command -v saml2aws)" ]; then
  CURR_VERSION=$(saml2aws --version 2>&1)
  echo "INFO: saml2aws installed: ${CURR_VERSION}"
else
  echo "INFO: saml2aws not installed"
fi

if [ "${VERSION}" != "${CURR_VERSION}" ]; then
  ZIP_FILE="https://github.com/Versent/saml2aws/releases/download/v${VERSION}/saml2aws_${VERSION}_linux_amd64.tar.gz"

  echo "INFO: Downloading saml2aws"
  cd /tmp
  [ -f ${ZIP_FILE} ] || wget ${ZIP_FILE} -q --no-check-certificate
  tar xfz saml2aws_${VERSION}_linux_amd64.tar.gz
  rm saml2aws_${VERSION}_linux_amd64.tar.*
  cd - 1> /dev/null

  echo "INFO: Installing to ${HOME}/.local/bin/"
  mkdir -p ${HOME}/.local/bin
  mv /tmp/saml2aws ${HOME}/.local/bin/

  echo "INFO: saml2aws installed: $(saml2aws --version 2>&1)"

  echo "INFO TODO: saml2aws configure"
fi

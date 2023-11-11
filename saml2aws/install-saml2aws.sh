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
  echo "INFO: Downloading saml2aws"
  FILE_NAME=saml2aws_${VERSION}_linux_amd64.tar.gz
  FILE_URL="https://github.com/Versent/saml2aws/releases/download/v${VERSION}/${FILE_NAME}"
  WORK_DIR=/tmp/tmp_workdir

  wget ${FILE_URL} -O /tmp/${FILE_NAME} --no-check-certificate -q
  mkdir -p ${WORK_DIR}
  tar xfz /tmp/${FILE_NAME} -C ${WORK_DIR}

  echo "INFO: Installing to ${HOME}/.local/bin/"
  mkdir -p ${HOME}/.local/bin
  mv ${WORK_DIR}/saml2aws ${HOME}/.local/bin/

  rm -rf ${WORK_DIR}

  echo "INFO: saml2aws installed: $(saml2aws --version 2>&1)"

  echo "INFO TODO: saml2aws configure"
fi

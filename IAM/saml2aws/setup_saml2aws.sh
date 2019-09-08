#!/bin/bash

VERSION=2.16.0
ZIP_FILE="https://github.com/Versent/saml2aws/releases/download/v${VERSION}/saml2aws_${VERSION}_linux_amd64.tar.gz"

# Download zip to home directory
pushd ~
[ -f ${ZIP_FILE} ] || wget ${ZIP_FILE}
tar xfz saml2aws_${VERSION}_linux_amd64.tar.gz
rm saml2aws_${VERSION}_linux_amd64.tar.*

# Copy binary to .local/bin and create a symlink for bookmarking the version
mkdir -p .local/bin
rm .local/bin/saml2aws || true
rm .local/bin/saml2aws-v${VERSION} || true

mv saml2aws .local/bin/
pushd .local/bin
ln -s saml2aws saml2aws-v${VERSION}
popd

popd

# Configure saml2aws
# saml2aws configure

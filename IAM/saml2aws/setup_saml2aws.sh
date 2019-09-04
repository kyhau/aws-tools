#!/bin/bash

cd ~
wget https://github.com/Versent/saml2aws/releases/download/v2.16.0/saml2aws_2.16.0_linux_amd64.tar.gz
tar xfz saml2aws_2.16.0_linux_amd64.tar.gz
mkdir -p .local/bin
cp saml2aws .local/bin/

# Configure saml2aws
# saml2aws configure

#!/bin/bash
set -e
# Modified from https://gist.github.com/riccardomc/a3891356b09516ab3f3b79a12e9b13e1
# See also https://aws.amazon.com/premiumsupport/knowledge-center/eks-error-invalid-identity-token/

[ -z "$DEBUG" ] || set -x

REGIONS="us-east-2
    us-east-1
    us-west-1
    us-west-2
    ap-southeast-1
    ap-southeast-2
    ap-southeast-3
    ap-southeast-4
    ap-northeast-1
    eu-central-1
    eu-west-1
    eu-west-2
    eu-west-3
    eu-north-1"

for REGION in $REGIONS ; do
  JWKS_URI="oidc.eks.${REGION}.amazonaws.com"

  # Extract all certificates in separate files
  # https://unix.stackexchange.com/questions/368123/how-to-extract-the-root-ca-and-subordinate-ca-from-a-certificate-chain-in-linux
  TEMP=$(mktemp -d -t oidc-eks-XXXX)
  openssl s_client -servername $JWKS_URI -showcerts -connect $JWKS_URI:443 < /dev/null 2>/dev/null | awk -v dir="$TEMP" '/-----BEGIN CERTIFICATE-----/,/-----END CERTIFICATE-----/{ if(/BEGIN/){a++}; out=dir"/cert00"a".crt"; print >out }'

  # Assume last found certificate in chain is the ROOT_CA
  ROOT_CA=$(ls -1 $TEMP/* | tail -1)

  # Extract thumbprint in desired format (no header, no colons)
  THUMBPRINT=$(openssl x509 -fingerprint -noout -in $ROOT_CA | sed 's/^.*=//' | sed 's/://g')
  printf '{"%s": "%s"}\n' $REGION $THUMBPRINT
  rm -rf $TEMP
done

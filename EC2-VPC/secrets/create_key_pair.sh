#!/bin/bash
set -e

KEY_NAME="MyKeyPair"

aws ec2 create-key-pair --key-name ${KEY_NAME} --query 'KeyMaterial' --output text > ${KEY_NAME}.pem

chmod 400 MyKeyPair.pem

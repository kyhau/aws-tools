#!/bin/bash
# Set to fail script if any command fails.
set -e

print_line() {
  printf "$(date +%Y-%m-%dT%H:%M:%S%z): $1\n"
}

# Parse arguments
PROFILE="default"
REGION="ap-southeast-2"

# Define the help menu
help_menu() {
  echo "Usage:
  ${0##*/}
    -n|--key-name KEY_NAME  Key name.
    -r|--profile PROFILE    AWS profile. Default ${PROFILE}.
    -r|--region REGION      AWS region. Default ${REGION}.
  "
  exit
}

while [[ "$#" > 0 ]]; do case $1 in
    -n|--key-name)       KEY_NAME="${2}"     ; shift ;;
    -r|--profile)        PROFILE="${2}"      ; shift ;;
    -r|--region)         REGION="${2}"       ; shift ;;
    -h|--help)           help_menu           ;;
    *)                   echo "Invalid option: ${1}" && help_menu ;;
esac; shift; done

[[ ! -z "$KEY_NAME" ]] || (echo "Error: KEY_NAME is not provided. Aborted." && exit 1)

if aws ec2 create-key-pair --key-name ${KEY_NAME} --query 'KeyMaterial' --output text --region $REGION --profile $PROFILE > ${KEY_NAME}.pem; then
  chmod 400 ${KEY_NAME}.pem
  print_line "Created ${KEY_NAME}.pem"
else
  echo "Error: Failed to create key pair ${KEY_NAME}"
  exit 1
fi

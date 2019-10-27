#!/bin/bash
# Set to fail script if any command fails.
set -e

# Define the help menu
help_menu() {
  echo "Usage:
  ${0##*/}
    --name-only    Name only
  "
  exit
}

# Parse arguments
NAME_ONLY=false

while [[ "$#" > 0 ]]; do case $1 in
    --name-only)         NAME_ONLY=true                          ;;
    -h|--help)           help_menu                                ;;
    *)                   echo "Invalid option: ${1}" && help_menu ;;
esac; shift; done

if [[ $NAME_ONLY = true ]]; then
  awk -F' ' '{for (i = 0; ++i <= NF;) print $i}' <<< $(
    aws ec2 describe-vpc-endpoint-services --query 'ServiceNames[*]' --output text
  )
else
  aws ec2 describe-vpc-endpoint-services
fi

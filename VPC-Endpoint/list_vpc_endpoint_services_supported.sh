#!/bin/bash

# Define the help menu
help_menu() {
  echo "Usage:
  ${0##*/}
    --profile      profile_name (optional)
    --name-only    Name-only (optional)
  "
  return
}

# Parse arguments
NAME_ONLY=false
PROFILE=default

while [[ "$#" > 0 ]]; do case $1 in
    --profile)           PROFILE="${2}"                   ; shift ;;
    --name-only)         NAME_ONLY=true                           ;;
    -h|--help)           help_menu                                ;;
    *)                   echo "Invalid option: ${1}" && help_menu ;;
esac; shift; done

if [[ $NAME_ONLY = true ]]; then
  awk -F' ' '{for (i = 0; ++i <= NF;) print $i}' <<< $(
    aws ec2 describe-vpc-endpoint-services --query 'ServiceNames[*]' --output text --profile $PROFILE
  )
else
  aws ec2 describe-vpc-endpoint-services --profile $PROFILE
fi

return

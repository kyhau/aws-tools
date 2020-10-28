#!/bin/bash

if [ $# -eq 0 ]; then

  # Retrieve all profile names (except default) from the default aws credentials file
  # and call the command for each profile
  while IFS="" read -r p || [ -n "$p" ]; do \
    aws ec2 describe-subnets --query 'Subnets[*].[OwnerId,SubnetId,AvailableIpAddressCount,CidrBlock]' --output text --profile $p
  done < <(cat ~/.aws/credentials | grep "\[" | tr -d '[]' | grep -v default)

else
  # Pass in "--profile <profile>" if needed
  aws ec2 describe-subnets --query 'Subnets[*].[OwnerId,SubnetId,AvailableIpAddressCount,CidrBlock]' --output text "$@"
fi

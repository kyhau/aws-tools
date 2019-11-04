#!/bin/bash

# Pass in "--profile <profile>" if needed

aws ec2 describe-subnets --query 'Subnets[*].[OwnerId,SubnetId,AvailableIpAddressCount,CidrBlock]' --output text "$@"

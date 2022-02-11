#!/bin/bash

# Find IP in security group

PROFILE=TODO

aws ec2 describe-security-groups --profile ${PROFILE} --filters \
  Name=ip-permission.from-port,Values=22 \
  Name=ip-permission.cidr,Values='61.11.11.11/32' \
  Name=ip-permission.cidr,Values='61.22.22.22/32' \
  --query SecurityGroups[*].{groupId:GroupId}

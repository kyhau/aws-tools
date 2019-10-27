#!/bin/bash
# Set to fail script if any command fails.
set -e

awk -F' ' '{for (i = 0; ++i <= NF;) print $i}' <<< $(
  aws ec2 describe-vpc-endpoint-services --query 'ServiceNames[*]' --output text
)

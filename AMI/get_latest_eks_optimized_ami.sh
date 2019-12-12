#!/bin/bash
# Return the latest ami-id of the EKS Optimised Amazon Linux 2 AMI
# Assume region ap-southeast-2
# https://docs.aws.amazon.com/eks/latest/userguide/eks-optimized-ami.html

latest_ami=$(aws ssm get-parameters "$@" --names /aws/service/eks/optimized-ami/1.14/amazon-linux-2/recommended/image_id --region ap-southeast-2 --query "Parameters[0].Value" | awk -F \" '{print $2}')
echo "$latest_ami"

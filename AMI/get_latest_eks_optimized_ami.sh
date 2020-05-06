#!/bin/bash
# Return the latest ami-id of the EKS Optimised Amazon Linux 2 AMI
# https://docs.aws.amazon.com/eks/latest/userguide/eks-optimized-ami.html

aws ssm get-parameters "$@" --names /aws/service/eks/optimized-ami/1.14/amazon-linux-2/recommended/image_id --query "Parameters[0].Value" --output text

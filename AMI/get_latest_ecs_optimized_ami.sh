#!/bin/bash
# Return the latest ami-id of the ECS Optimised Amazon Linux 2 AMI
# Assume region ap-southeast-2

latest_ami=$(aws ssm get-parameters "$@" --names /aws/service/ecs/optimized-ami/amazon-linux-2/recommended/image_id --region ap-southeast-2 --query "Parameters[0].Value" | awk -F \" '{print $2}')
echo "$latest_ami"

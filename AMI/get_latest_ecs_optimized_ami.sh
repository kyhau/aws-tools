#!/bin/bash
# Return the latest ami-id of the ECS Optimised Amazon Linux 2 AMI

aws ssm get-parameters "$@" --names /aws/service/ecs/optimized-ami/amazon-linux-2/recommended/image_id --query "Parameters[0].Value" --output text


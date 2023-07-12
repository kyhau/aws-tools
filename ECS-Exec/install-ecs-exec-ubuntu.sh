#!/bin/bash
# https://aws.amazon.com/blogs/containers/new-using-amazon-ecs-exec-access-your-containers-fargate-ec2/

set -e

REPO_HOME=$(dirname $(dirname $(realpath $0)))

# Install the Session Manager plugin on Ubuntu Server
. ${REPO_HOME}/SSM/install-aws-session-manager-plugin-ubuntu.sh

# Install awscli v1 (v2 coming soon)
# This version includes the additional ECS Exec logic and the ability to hook the Session Manager plugin to initiate the secure connection into the container.
pip install -U awscli

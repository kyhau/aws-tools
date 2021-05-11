#!/bin/bash
# https://aws.amazon.com/blogs/containers/new-using-amazon-ecs-exec-access-your-containers-fargate-ec2/

set -e

####
# Install the Session Manager plugin on Ubuntu Server
# Download the Session Manager plugin deb package.
curl "https://s3.amazonaws.com/session-manager-downloads/plugin/latest/ubuntu_64bit/session-manager-plugin.deb" -o "session-manager-plugin.deb"
# Run the install command.
sudo dpkg -i session-manager-plugin.deb
# Verify the Session Manager plugin installation
session-manager-plugin
rm session-manager-plugin.deb

####
# Install awscli v1 (v2 coming soon)
# This version includes the additional ECS Exec logic and the ability to hook the Session Manager plugin to initiate the secure connection into the container.
pip install -U awscli

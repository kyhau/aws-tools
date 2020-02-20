#!/bin/bash

# https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-manual-agent-install.html

# Check centos version
cat /etc/system-release

# CentOS 7.x:
sudo systemctl status amazon-ssm-agent

# CentOS 6.x:
#sudo status amazon-ssm-agent

# Check 64 or 32
uname -m

# 64-bit instances:
sudo yum install -y https://s3.amazonaws.com/ec2-downloads-windows/SSMAgent/latest/linux_amd64/amazon-ssm-agent.rpm

# 32-bit instances:
sudo yum install -y https://s3.amazonaws.com/ec2-downloads-windows/SSMAgent/latest/linux_386/amazon-ssm-agent.rpm

# Check the status again, if not started, start it.
sudo systemctl status amazon-ssm-agent

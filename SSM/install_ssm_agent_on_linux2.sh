#!/bin/bash

# https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-manual-agent-install.html

# Check status
sudo systemctl status amazon-ssm-agent

# version
yum info amazon-ssm-agent

# check intel or ARM
uname -a

# update
# Intel (x86_64) 64-bit instances:
sudo yum install -y https://s3.amazonaws.com/ec2-downloads-windows/SSMAgent/latest/linux_amd64/amazon-ssm-agent.rpm

# ARM (arm64) 64-bit instances:
#sudo yum install -y https://s3.amazonaws.com/ec2-downloads-windows/SSMAgent/latest/linux_arm64/amazon-ssm-agent.rpm

# Intel (x86) 32-bit instances:
#sudo yum install -y https://s3.amazonaws.com/ec2-do wnloads-windows/SSMAgent/latest/linux_386/amazon-ssm-agent.rpm

sudo systemctl enable amazon-ssm-agent
sudo systemctl status amazon-ssm-agent

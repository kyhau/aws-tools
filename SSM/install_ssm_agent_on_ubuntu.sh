#!/bin/bash

# https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-manual-agent-install.html

# Check version
lsb_release -a

# Check 64 or 32
uname -i

# Install snap
sudo apt install snapd

# Install amazon-ssm-agent using snap
sudo snap install amazon-ssm-agent --classic

# Or, udpate
sudo snap refresh amazon-ssm-agent

sudo systemctl status snap.amazon-ssm-agent.amazon-ssm-agent.service
sudo snap services amazon-ssm-agent

#!/bin/bash
# https://aws.amazon.com/blogs/containers/announcing-the-amazon-ecs-cli-v2/

set -e

echo "Downloading the latest version..."
wget https://github.com/aws/amazon-ecs-cli-v2/releases/download/v0.0.4/ecs-preview-linux-v0.0.4
chmod +x ecs-preview-linux-v0.0.4

echo "Coping binary to .local/bin..."
mkdir -p ~/.local/bin
sudo cp ecs-preview-linux-v0.0.4 ~/.local/bin/ecs
#sudo cp ecs-preview-linux-v0.0.4 /usr/local/bin/ecs

echo "Checking version..."
ecs version

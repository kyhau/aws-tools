#!/bin/bash
# https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ECS_CLI_installation.html

set -e

echo "INFO: Downloading ECS CLI"
mkdir -p ~/.local/bin
curl -Lo ecs-cli https://amazon-ecs-cli.s3.amazonaws.com/ecs-cli-linux-amd64-latest
chmod +x ecs-cli

echo "INFO: Moving binary to ~/.local/bin"
mkdir -p ~/.local/bin
mv ecs-cli ~/.local/bin/ecs-cli

echo "INFO: Checking version"
echo "ecs-cli version: $(ecs-cli --version)"

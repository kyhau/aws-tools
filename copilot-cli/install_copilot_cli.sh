#!/bin/bash
# https://github.com/aws/copilot-cli
set -e

brew install aws/tap/copilot-cli
brew upgrade aws/tap/copilot-cli

# OR
# Check version here https://github.com/aws/copilot-cli/tags
#
# sudo curl -Lo /usr/local/bin/copilot https://github.com/aws/copilot-cli/releases/download/v0.4.0/copilot-linux-v0.4.0 && sudo chmod +x /usr/local/bin/copilot && copilot --help

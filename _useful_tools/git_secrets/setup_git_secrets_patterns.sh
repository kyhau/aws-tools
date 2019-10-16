#!/bin/bash
# Set to fail script if any command fails.
set -e

# Add some global allowed patterns

# Fake aws account id
git secrets --add --global --allowed '111122223333'

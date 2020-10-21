#!/bin/bash
# See also https://github.com/nodesource/distributions#debmanual

VERSION=15.x

# Remove current installations, if any
sudo apt-get --purge remove node

curl -sL https://deb.nodesource.com/setup_${VERSION} | sudo -E bash -
sudo apt-get install -y nodejs

echo "node version: $(node --version)"
echo "npm version: $(npm --version)"

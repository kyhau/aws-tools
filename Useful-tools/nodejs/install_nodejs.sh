#!/bin/bash
# See also https://github.com/nodesource/distributions#debmanual

# Remove current installations, if any
sudo apt-get --purge remove node
# ("sudo apt autoremove node" if console is asking for)

VERSION=node_13.x

# Add the NodeSource package signing key
curl -sSL https://deb.nodesource.com/gpgkey/nodesource.gpg.key | sudo apt-key add -

# Add the desired NodeSource repository
DISTRO="$(lsb_release -s -c)"
echo "deb https://deb.nodesource.com/$VERSION $DISTRO main" | sudo tee /etc/apt/sources.list.d/nodesource.list
echo "deb-src https://deb.nodesource.com/$VERSION $DISTRO main" | sudo tee -a /etc/apt/sources.list.d/nodesource.list

#curl -sL https://deb.nodesource.com/setup_13.x | sudo -E bash -

# Update package lists and install Node.js
sudo sudo apt update
sudo apt-get install -y nodejs
#sudo apt-get install -y npm
sudo apt-get -y autoremove

# Then install build tools so you can install add-ons for npm later
# sudo apt-get install -y build-essential

echo "npm version: `npm -v`"
echo "node version: `node -v`"

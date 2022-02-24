#!/bin/bash
set -e
# See https://docs.microsoft.com/en-us/powershell/scripting/install/install-ubuntu

# Update the list of packages
sudo apt-get update
# Install pre-requisite packages.
sudo apt-get install -y wget apt-transport-https software-properties-common
# Download the Microsoft repository GPG keys
wget -q https://packages.microsoft.com/config/ubuntu/20.04/packages-microsoft-prod.deb
# Register the Microsoft repository GPG keys
sudo dpkg -i packages-microsoft-prod.deb
# Update the list of packages after we added packages.microsoft.com
sudo apt-get update
# Install PowerShell
sudo apt-get install -y powershell
# Clean up
rm packages-microsoft-prod.deb
# Start PowerShell
echo "INFO: To start Powershell: pwsh"
# pwsh

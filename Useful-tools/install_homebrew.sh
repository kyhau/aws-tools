#!/bin/bash
# Install Homebrew on Ubuntu
# https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install-linux.html
set -e

echo "CheckPt: Install Homebrew to /home/linuxbrew/.linuxbrew (default)"
sh -c "$(curl -fsSL https://raw.githubusercontent.com/Linuxbrew/install/master/install.sh)"

# Add Homebrew to your PATH by running the following commands. These commands work on all major flavors of Linux by
# adding either ~/.profile on Debian/Ubuntu or ~/.bash_profile on CentOS/Fedora/RedHat:
echo "CheckPt: Add Homebrew to your PATH"
test -d ~/.linuxbrew && eval $(~/.linuxbrew/bin/brew shellenv)
test -d /home/linuxbrew/.linuxbrew && eval $(/home/linuxbrew/.linuxbrew/bin/brew shellenv)
test -r ~/.bash_profile && echo "eval \$($(brew --prefix)/bin/brew shellenv)" >>~/.bash_profile
echo "eval \$($(brew --prefix)/bin/brew shellenv)" >>~/.profile

echo "CheckPt: Verify that Homebrew is installed"
brew --version

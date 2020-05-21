#!/bin/bash
# See:
# How do I troubleshoot network performance issues between EC2 Linux instances in a VPC and
# an on-premises host over the internet gateway?
# https://aws.amazon.com/premiumsupport/knowledge-center/network-issue-vpc-onprem-ig/

set -e

PKG_MANAGER=$( command -v yum || command -v apt-get ) || echo "Neither yum nor apt-get found. Aborted" && exit 1
echo "Package Manager: ${PKG_MANAGER}"

# Test performance using MTRTest performance using MTR
echo "Installing mtr..."
sudo ${PKG_MANAGER} install mtr

# Test performance using traceroute
# Traceroute is not necessary if an MTR report is executed. MTR provides latency and packet loss statistics to
# a destination.
echo "Installing traceroute..."
sudo ${PKG_MANAGER} install traceroute

# Test packet capture samples using tcpdump
echo "Installing tcpdump..."
sudo ${PKG_MANAGER} install tcpdump

#  Test performance using hping3
# MTRs and traceroute capture per-hop latency. However, hping3 yields results that show end-to-end min/avg/max
# latency over TCP in addition to packet loss.
echo "Installing hping3..."
if [[ "$PKG_MANAGER" = *"apt-get"*  ]]; then
  sudo ${PKG_MANAGER} install hping3
else
  sudo ${PKG_MANAGER} --enablerepo=epel install hping3
fi

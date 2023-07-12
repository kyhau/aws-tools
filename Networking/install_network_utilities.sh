#!/bin/bash
# See:
# How do I troubleshoot network performance issues between EC2 Linux instances in a VPC and
# an on-premises host over the internet gateway?
# https://aws.amazon.com/premiumsupport/knowledge-center/network-issue-vpc-onprem-ig/
set -e

PKG_MANAGER=$( command -v yum || command -v apt-get ) || echo "Neither yum nor apt-get found. Aborted" && exit 1
echo "Package Manager: ${PKG_MANAGER}"

install_something() {
  tool_name=${1}
  echo "Installing ${tool_name}..."
  sudo ${PKG_MANAGER} install ${tool_name} -y
}

install_hping3() {
  echo "Installing hping3..."
  if [[ "$PKG_MANAGER" = *"apt-get"*  ]]; then
    sudo ${PKG_MANAGER} install hping3 -y
  else
    sudo ${PKG_MANAGER} --enablerepo=epel install hping3 -y
  fi
}

# Test performance using MTRTest performance using MTR
install_something "mtr"

# Test performance using traceroute
# Traceroute is not necessary if an MTR report is executed. MTR provides latency and packet loss statistics to
# a destination.
install_something "traceroute"

# Test packet capture samples using tcpdump
install_something "tcpdump"

# Test performance using hping3
# MTRs and traceroute capture per-hop latency. However, hping3 yields results that show end-to-end min/avg/max
# latency over TCP in addition to packet loss.
install_something "hping3"

# iptraf – tcp/udp network monitoring utility
install_something "iptraf"

# tc (Traffic Control) is a useful utility that gives you the ability to configure the kernel packet scheduler.
# tc comes bundled with iproute
install_something "iproute"

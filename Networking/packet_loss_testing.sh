#!/bin/bash
# Ref: https://sandilands.info/sgordon/dropping-packets-in-ubuntu-linux-using-tc-and-iptables

set -e

################################################################################
# On computer B (the destination), to view the current set of rules:
sudo iptables -L

# Dropping Packets with iptables
# Now to add a rule to the INPUT chain to drop 5% of incoming packets on computer B:
sudo iptables -A INPUT -m statistic --mode random --probability 0.05 -j DROP

# Returning to computer B, to delete a rule you can use the -D option:
sudo iptables -D INPUT -m statistic --mode random --probability 0.05 -j DROP

################################################################################
# Check "retransmitted"
netstat -s | grep retra

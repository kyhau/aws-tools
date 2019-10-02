#!/bin/bash

sudo yum install tcpdump

# Listen to all ssh traffic
sudo tcpdump port 22

# Log all details to file
sudo tcpdump -X -w packets.txt

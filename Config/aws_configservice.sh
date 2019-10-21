#!/bin/bash
# Set to fail script if any command fails.
set -e

aws configservice select-resource-config --expression "$(cat ec2.sql)"

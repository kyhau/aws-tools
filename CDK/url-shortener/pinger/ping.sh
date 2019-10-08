#!/bin/sh
# Set to fail script if any command fails.
set -e

while true; do
  curl -i $URL
  sleep 1
done

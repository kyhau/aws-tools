#!/bin/bash
# Set to fail script if any command fails.
set -e

mysql --user=admin --password -h tsagallery-database-cluster.cluster-cmgqhhgauxxx.ap-southeast-1.rds.amazonaws.com

# show databases;

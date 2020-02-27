#!/bin/bash
# Set to fail script if any command fails.
set -e

cp infra-lab8.yml infra.yml
zip infra.yml.zip infra.yml

aws s3 cp infra.yml.zip s3://xxxtsagallery.companyname.com/cloudformation/

rm infra.yml.zip infra.yml

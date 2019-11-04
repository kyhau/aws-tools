#!/bin/bash
# Set to fail script if any command fails.
set -e

aws --region us-east-1 serverlessrepo create-cloud-formation-template --application-id arn:aws:serverlessrepo:us-east-1:903779448426:applications/lambda-layer-awscli
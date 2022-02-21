#!/bin/bash
set -e

BUCKET_PATH="s3://runner-build-common-imagebuilderlogbucket-xxx/runner-amazonlinux2min-x86-ec2/"
rm -rf k-tmp-s3-files/*
aws s3 sync "$BUCKET_PATH" k-tmp-s3-files/

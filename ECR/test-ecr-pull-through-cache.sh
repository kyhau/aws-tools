#!/bin/bash
set -e

AWS_REGION=ap-southeast-2
PRIV_REGISTRY=123456789012.dkr.ecr.${AWS_REGION}.amazonaws.com

aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${PRIV_REGISTRY}

docker pull ${PRIV_REGISTRY}/ecr-public/amazonlinux/amazonlinux:latest

#!/bin/bash
set -e
# Ref: https://docs.aws.amazon.com/eks/latest/userguide/copy-image-to-repository.html

AWS_REGION=ap-southeast-2
PRIV_REGISTRY=123456789012.dkr.ecr.${AWS_REGION}.amazonaws.com
FROM_IMAGE=pingidentity/pingfederate
IMAGE_VERSION=11.2.4-alpine_3.17.3-al11-x86_64-edge
TO_IMAGE=external/${FROM_IMAGE}

aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${PRIV_REGISTRY}

docker pull ${FROM_IMAGE}:${IMAGE_VERSION}

aws ecr create-repository --repository-name ${TO_IMAGE}

docker tag ${FROM_IMAGE}:${IMAGE_VERSION} ${PRIV_REGISTRY}/${TO_IMAGE}:${IMAGE_VERSION}

docker push ${PRIV_REGISTRY}/${TO_IMAGE}:${IMAGE_VERSION}

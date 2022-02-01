#!/bin/bash
# https://docs.aws.amazon.com/step-functions/latest/dg/sfn-local-docker.html

docker pull amazon/aws-stepfunctions-local
docker run -p 8083:8083 amazon/aws-stepfunctions-local

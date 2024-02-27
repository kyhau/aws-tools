#!/bin/bash
set -e

aws ecr describe-pull-through-cache-rules

aws ecr create-pull-through-cache-rule --ecr-repository-prefix ecr-public --upstream-registry-url public.ecr.aws --region ap-southeast-2

# aws ecr create-pull-through-cache-rule --ecr-repository-prefix docker-hub --upstream-registry-url registry-1.docker.io --region ap-southeast-2

aws ecr validate-pull-through-cache-rule --ecr-repository-prefix ecr-public --region ap-southeast-2



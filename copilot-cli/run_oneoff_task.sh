#!/bin/bash
# Run a task using your local Dockerfile with ECS Fargate.
# Fro details see https://github.com/aws/copilot-cli/wiki/task-run-command

# If using --default and you get an error saying there's no default cluster, run aws ecs create-cluster and then re-run the copilot command.
# aws ecs create-cluster

copilot task run --default --follow --task-group-name "k-task-group-1" --image alpine:latest --command "ls -al"

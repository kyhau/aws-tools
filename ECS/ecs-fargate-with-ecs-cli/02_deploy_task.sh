#!/bin/bash
set -e

# Edit ecs-params.yml

ConfigName=k-test-ecs-fargate
ProfileName=ecs-profile

# Deploy the Compose File to a Cluster

# By default, the command looks for files called docker-compose.yml and ecs-params.yml in the current directory;
# you can specify a different docker compose file with the --file option, and a different ECS Params file with the --ecs-params option

ecs-cli compose --project-name ${ConfigName} service up --create-log-groups --cluster-config ${ConfigName} --ecs-profile ${ProfileName}

# After you deploy the compose file, you can view the containers that are running in the service with ecs-cli compose service ps.
ecs-cli compose --project-name ${ConfigName} service ps --cluster-config ${ConfigName} --ecs-profile ${ProfileName}

# View the Container Logs
# ecs-cli logs --task-id 0c2862e6e39e4eff92ca3e4f843c5b9a --follow --cluster-config ${ConfigName} --ecs-profile ${ProfileName}

# View the Web Application
# Enter the IP address for the task in your web browser and you should see a webpage that displays the Simple PHP App web application.
# see https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-cli-tutorial-fargate.html

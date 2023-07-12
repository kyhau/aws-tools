#!/bin/bash
set -e

ConfigName=k-test-ecs-fargate
ProfileName=ecs-profile

# To increase running count of the application to two
ecs-cli compose --project-name ${ConfigName} service scale 2 --cluster-config ${ConfigName} --ecs-profile ${ProfileName}

# Check if two more containers in your cluster
ecs-cli compose --project-name ${ConfigName}  service ps --cluster-config ${ConfigName} --ecs-profile ${ProfileName}

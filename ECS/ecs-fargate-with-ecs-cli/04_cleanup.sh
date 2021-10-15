#!/bin/bash
set -e

RoleName=K-Test-EcsTaskExecutionRole
ConfigName=k-test-ecs-fargate
ProfileName=ecs-profile

ecs-cli compose --project-name ${ConfigName} service down --cluster-config ${ConfigName} --ecs-profile ${ProfileName}

ecs-cli down --force --cluster-config ${ConfigName} --ecs-profile ${ProfileName}

aws iam detach-role-policy --role-name ${RoleName} --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy

aws iam delete-role --role-name ${RoleName}

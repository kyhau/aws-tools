#!/bin/bash
set -e

AWS_ACCESS_KEY_ID=  # TODO
AWS_SECRET_ACCESS_KEY=  # TODO
RoleName=K-Test-EcsTaskExecutionRole
ClusterName=k-test-ecs-fargate
ConfigName=k-test-ecs-fargate
Region=ap-southeast-2
ProfileName=ecs-profile

# Create a file named task-execution-assume-role.json
aws iam create-role --role-name ${RoleName} --assume-role-policy-document file://task-execution-assume-role.json

# Attach the task execution role policy
aws iam attach-role-policy --role-name ${RoleName} --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy

# Create a cluster configuration: ~/.ecs/config
ecs-cli configure --cluster${ClusterName} --default-launch-type FARGATE --config-name ${ConfigName} --region ${Region}

# TODO
# Create a CLI profile using your access key and secret key
ecs-cli configure profile --access-key ${AWS_ACCESS_KEY_ID} --secret-key ${AWS_SECRET_ACCESS_KEY} --profile-name ${ProfileName}

# Create an Amazon ECS cluster.
# Because you specified Fargate as your default launch type in the cluster configuration, this command creates an empty cluster and a VPC configured with two public subnets.
ecs-cli up --cluster-config ${ConfigName} --ecs-profile ${ProfileName}

VpcId=$(aws cloudformation describe-stack-resources --stack-name amazon-ecs-cli-setup-${ClusterName} | jq -r '.StackResources[] | select(.ResourceType == "AWS::EC2::VPC") | .PhysicalResourceId')

# Retrieve the default security group ID for the VPC

SgId=$(aws ec2 describe-security-groups --filters Name=vpc-id,Values=${VpcId} --region ${Region} | jq -r '.SecurityGroups[] | select(.GroupName ) | .GroupId' )

# Add a security group rule to allow inbound access on port 80
aws ec2 authorize-security-group-ingress --group-id ${SgId} --protocol tcp --port 80 --cidr 0.0.0.0/0 --region ${Region}

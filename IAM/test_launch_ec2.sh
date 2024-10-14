#!/bin/bash
set -e

AWS_PROFILE=TODO
AWS_REGION=TODO
VPC_ID=TODO
AMI_ID=TODO

aws ec2 create-key-pair --key-name poc-testing --query 'KeyMaterial' --output text > poc-testing-keypair.pem

aws ec2 create-security-group --group-name poc-testing-sg --description "poc-testing-sg" --vpc-id $VPC_ID

SG_ID=TODO

aws ec2 authorize-security-group-ingress --group-name poc-testing-sg --protocol tcp --port 22 --cidr 0.0.0.0/0

aws ec2 describe-security-groups --group-ids $SG_ID

SUBNET_ID=TODO

aws ec2 run-instances --image-id $AMI_ID --count 10 --instance-type t3.medium --key-name poc-testing --security-group-ids $SG_ID --subnet-id $SUBNET_ID --region $AWS_REGION

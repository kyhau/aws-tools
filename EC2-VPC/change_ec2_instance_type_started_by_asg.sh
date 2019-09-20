#!/bin/bash
# This script intends to change the instance type of an instance started by Auto Scaling Group.
# It does not change the existing Launch Configuration in the Auto Scaling Group.

# Set to fail script if any command fails.
set -e

# Define the help menu
help_menu() {
  echo "Usage:
  ${0##*/}
    --name-tag NAME_TAG              A tag for searching ASG / EC2 name
    --instance-type INSTANCE_TYPE    The target instance type for the primary node; e.g. r3.medium
  "
  exit
}

# Parse arguments
while [[ "$#" -gt 0 ]]; do case $1 in
    --name-tag)       NAME_TAG="${2}"                  ; shift ;;
    --instance-type)  INSTANCE_TYPE="${2}"             ; shift ;;
    -h|--help)        help_menu                                ;;
    *)                echo "Invalid option: ${1}" && help_menu ;;
esac; shift; done

[[ ! -z "NAME_TAG" ]] || (echo "Error: NAME_TAG is not provided. Aborted." && exit 1)
[[ ! -z "$INSTANCE_TYPE" ]] || (echo "Error: INSTANCE_TYPE is not provided. Aborted." && exit 1)


NAME_TAG="informix-${APP_NAME}-${STAGE_NAME}-${STACK_NAME}-db-ha1"

# Find Instance ID and check instance type
{
  ec2_instance=$(aws ec2 describe-instances \
    --query 'Reservations[*].Instances[*].[InstanceType,InstanceId,Tags[?Key==`Name`] | [0].Value]' --output text \
    | grep "$NAME_TAG")
} || (echo "Error: Instance with prefix (${NAME_TAG}) not found. Aborted." && exit 1)

instance_type=$(echo ${ec2_instance} | cut -d' ' -f1)
instance_id=$(echo ${ec2_instance} | cut -d' ' -f2)
instance_name=$(echo ${ec2_instance} | cut -d' ' -f3)

# No need to continue if the instance is currently using the target instance type already
[ "$instance_type" != "$INSTANCE_TYPE" ] || (echo "Already running with target instance type. Exit now." && exit 0)

echo "Started updating instance ${instance_name} (${instance_id}) from ${instance_type} to ${INSTANCE_TYPE}..."

# Find auto scaling group name
{
  asg_name=$(aws autoscaling describe-auto-scaling-groups  \
    --query 'AutoScalingGroups[].[AutoScalingGroupName]' --output text \
    | grep "$NAME_TAG")
} || (echo "Error: Auto Scaling Group with prefix (${NAME_TAG}) not found. Aborted." && exit 1)

echo "Suspending processes on Auto Scaling Group $asg_name..."
{
  # No output from aws cli command but the change is applied instantly.
  aws autoscaling suspend-processes --auto-scaling-group-name "$asg_name"
} || (echo "Error: Unable to suspend Auto Scaling Group ($asg_name). Aborted." && exit 1)

echo "Stopping EC2 instance $instance_id..."
{
  aws ec2 stop-instances --instance-ids "$instance_id"
} || (echo "Error: Unable to stop instance ($instance_id). Aborted." && exit 1)

aws ec2 wait instance-stopped --instance-ids "$instance_id"
echo "Confirmed EC2 instance $instance_id is stopped."

echo "Updating instance ${instance_name} (${instance_id}) from ${instance_type} to ${INSTANCE_TYPE}..."
{
  aws ec2 modify-instance-attribute --instance-id "$instance_id" \
    --instance-type "{\"Value\": \"${INSTANCE_TYPE}\"}"
} || (echo "Error: Unable to change instance type for ($instance_id). Aborted." && exit 1)

echo "Starting EC2 instance ${instance_id}..."
{
  aws ec2 start-instances --instance-ids "$instance_id"
} || (echo "Error: Unable to start instance ($instance_id). Aborted." && exit 1)

aws ec2 wait instance-running --instance-ids "$instance_id"
echo "Confirmed EC2 instance ${instance_id} is running."

aws ec2 wait instance-status-ok --instance-ids "$instance_id"
echo "Confirmed EC2 instance ${instance_id} status OK."

echo "Resuming processes on Auto Scaling Group $asg_name..."
{
  aws autoscaling resume-processes --auto-scaling-group-name "$asg_name"
} || (echo "Error: Unable to resume Auto Scaling Group ($asg_name). Aborted." && exit 1)

echo "All done."

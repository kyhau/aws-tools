# ECS

```
################################################################################

# Retrieve the latest ECS–optimized AMI metadata
aws ssm get-parameters --names /aws/service/ecs/optimized-ami/amazon-linux-2/recommended --query "Parameters[].Value" --output text | jq .

# Get the latest ECS Optimized AMI (Amazon Linux 2) image_id
aws ssm get-parameters --names /aws/service/ecs/optimized-ami/amazon-linux-2/recommended/image_id --region ap-southeast-2 --query "Parameters[0].Value" | awk -F \" '{print $2}'

# Find all outdated container instances
aws ecs list-container-instances --cluster <cluster name> --filter "attribute:ecs.ami-id != <image_id>"

# Find the corresponding EC2 instance IDs for these container instances. 
# The IDs are then used to find the corresponding Auto Scaling group from which to detach the instances.

aws ecs list-container-instances --cluster <cluster name> --filter "attribute:ecs.ami-id != <image_id>"| \
jq -c '.containerInstanceArns[]' | \
xargs aws ecs describe-container-instances --cluster <cluster name> --container-instances | \
jq '[.containerInstances[]|{(.containerInstanceArn) : .ec2InstanceId}]'

# List the instances that are part of an Auto Scaling group
aws autoscaling describe-auto-scaling-instances --instance-ids <instance id #1> <instance id #2>

```

See also

1. [Amazon ECS-optimized AMIs](
https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html
)

1. [Refreshing an Amazon ECS Container Instance Cluster With a New AMI](
https://aws.amazon.com/blogs/compute/refreshing-an-amazon-ecs-container-instance-cluster-with-a-new-ami/
) - Nathan Taber, 14 AUG 2018
# ECS

Notes

1. Fargate 1.3 had two ENIs and some fun routing. Fargate 1.4 AWS put it back to single ENI (and if you put it in the VPC I think it wants endpoints).

Useful links

1. [ECS + CloudFormation without clobbering desired counts?](https://www.reddit.com/r/aws/comments/6pwxkv/ecs_cloudformation_without_clobbering_desired/)
    > I've run into this as well, the ECS services behave subtly different from the ASG scaling. In ASG if you don't set the DesiredCapacity (which isn't required) then CFN/ASG will happily keep the existing value. However the DesiredCount is required for ECS Services so CFN will honor what you've put in the template and happily reset your service back to what's in your template. Even if that means going from 20 instances to 1 in a heartbeat.

1. [How can I correctly update my Auto Scaling group when I update my AWS CloudFormation stack?](https://aws.amazon.com/premiumsupport/knowledge-center/auto-scaling-group-rolling-updates/)
1. [Refreshing an Amazon ECS Container Instance Cluster With a New AMI](https://aws.amazon.com/blogs/compute/refreshing-an-amazon-ecs-container-instance-cluster-with-a-new-ami/)


---

[Amazon ECS-optimized AMIs](https://docs.aws.amazon.com/AmazonECS/latest/developerguideecs-optimized_AMI.html)

```
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

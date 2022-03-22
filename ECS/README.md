# ECS Notes

- [Useful Libs and Tools](#useful-libs-and-tools)
- [Useful Articles and Blogs](#useful-articles-and-blogs)

---
## Useful Libs and Tools

- [amazon-ecs-cli-v2](https://aws.amazon.com/blogs/containers/announcing-the-amazon-ecs-cli-v2/) - Amazon ECS CLI v2
- [bottlerocket-ecs-updater](https://github.com/bottlerocket-os/bottlerocket-ecs-updater) - Bottlerocket ECS Updater is a service you can install into your ECS cluster that helps you keep your Bottlerocket container instances up to date.
- [copilot-cli](https://github.com/aws/copilot-cli) - AWS Copilot CLI - containerize apps on ECS/Fargate
- [aws-samples/aws-fargate-fast-autoscaler](https://github.com/aws-samples/aws-fargate-fast-autoscaler) = AWS Fargate Fast AutoScaler (with CDK)
- [docker/ecs-plugin](https://github.com/docker/ecs-plugin) - Docker CLI plugin for ECS


---
## Useful Articles and Blogs

1. Access
    1. [Using Amazon ECS Exec to access your containers on AWS Fargate and Amazon EC2](https://aws.amazon.com/blogs/containers/new-using-amazon-ecs-exec-access-your-containers-fargate-ec2/)
1. Fargate
    1. Fargate 1.3 had two ENIs and some fun routing. Fargate 1.4 AWS put it back to single ENI (and if you put it in the VPC I think it wants endpoints).
1. Cost
    1. [Theoretical cost optimization by Amazon ECS launch type: Fargate vs EC2](https://aws.amazon.com/blogs/containers/theoretical-cost-optimization-by-amazon-ecs-launch-type-fargate-vs-ec2/)
        - > For steady-state, predictable workload levels that use a higher proportion of the instance CPU and memory, EC2 can be a more cost-effective choice, as it is possible to simply select the instance type for which tasks can optimally use the available resources.
        - > For highly dynamic workloads where right-sizing and scaling EC2 infrastructure introduces the risks of under/over-provisioning, the flexibility in cost and operation provided by Fargate would be beneficial.
1. CloudFormation, ASG and desired count
    1. [ECS + CloudFormation without clobbering desired counts?](https://www.reddit.com/r/aws/comments/6pwxkv/ecs_cloudformation_without_clobbering_desired/)
        > I've run into this as well, the ECS services behave subtly different from the ASG scaling. In ASG if you don't set the DesiredCapacity (which isn't required) then CFN/ASG will happily keep the existing value. However the DesiredCount is required for ECS Services so CFN will honor what you've put in the template and happily reset your service back to what's in your template. Even if that means going from 20 instances to 1 in a heartbeat.
    1. [How can I correctly update my Auto Scaling group when I update my CloudFormation stack?](https://aws.amazon.com/premiumsupport/knowledge-center/auto-scaling-group-rolling-updates/)
    1. [Refreshing an Amazon ECS Container Instance Cluster With a New AMI](https://aws.amazon.com/blogs/compute/refreshing-an-amazon-ecs-container-instance-cluster-with-a-new-ami/)
1. ECS Cluster utilization and Service utilization
    - CPU Units example: A t3.medium has 2 vCPUs so it would be 2 x 1024 = 2048 CPU units
    - https://docs.aws.amazon.com/AmazonECS/latest/developerguide/cloudwatch-metrics.html#cluster_reservation
    - https://aws.amazon.com/blogs/containers/how-amazon-ecs-manages-cpu-and-memory-resources/
1. CDK
    - [aws_cdk.aws_ecs](https://docs.aws.amazon.com/cdk/api/latest/docs/aws-ecs-readme.html)
    - [aws_cdk.aws_ecs_patterns](https://docs.aws.amazon.com/cdk/api/latest/docs/aws-ecs-patterns-readme.html)
      This library provides higher-level Amazon ECS constructs which follow common architectural patterns. It contains:
       - Application Load Balanced Services
       - Network Load Balanced Services
       - Queue Processing Services
       - Scheduled Tasks (cron jobs)
1. MLA
    - Amazon ECS Log File Locations https://docs.aws.amazon.com/AmazonECS/latest/developerguide/logs.html
    - Amazon ECS Container Agent Configuration https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-agent-config.html
    - Example container instance user data configuration scripts https://docs.aws.amazon.com/AmazonECS/latest/developerguide/example_user_data_scripts.html
1. Amazon ECS-optimized AMIs
    1. https://docs.aws.amazon.com/AmazonECS/latest/developerguideecs-optimized_AMI.html

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

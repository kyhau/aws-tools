# ECS Notes

- [Useful Libs and Tools](#useful-libs-and-tools)
- [Useful Articles and Blogs](#useful-articles-and-blogs)
- [Fargate](#fargate)
    - [Mapping Fargate cpu to EC2 instance type](#mapping-fargate-cpu-to-ec2-instance-type)
- [Building Container images in containers](#building-container-images-in-containers)
- [ECS - ENI trunking](#ecs---eni-trunking)

---
## Useful Libs and Tools

- [amazon-ecs-cli-v2](https://aws.amazon.com/blogs/containers/announcing-the-amazon-ecs-cli-v2/) - Amazon ECS CLI v2
- [copilot-cli](https://github.com/aws/copilot-cli) - AWS Copilot CLI - containerize apps on ECS/Fargate
- [aws-samples/aws-fargate-fast-autoscaler](https://github.com/aws-samples/aws-fargate-fast-autoscaler) = AWS Fargate Fast AutoScaler (with CDK)
- [docker/ecs-plugin](https://github.com/docker/ecs-plugin) - Docker CLI plugin for ECS


---
## Useful Articles and Blogs

ℹ️ Predictive Auto-Scaling only supports by EC2, not ECS. See [Container Roadmap](https://github.com/aws/containers-roadmap/issues/1574)

- Scaling
    - [Scaling containers on AWS in 2022](https://www.vladionescu.me/posts/scaling-containers-on-aws-in-2022/)
- Access
    - [Using Amazon ECS Exec to access your containers on AWS Fargate and Amazon EC2](https://aws.amazon.com/blogs/containers/new-using-amazon-ecs-exec-access-your-containers-fargate-ec2/)
- Fargate
    - Fargate 1.3 had two ENIs and some fun routing. Fargate 1.4 AWS put it back to single ENI (and if you put it in the VPC I think it wants endpoints).
- Cost
    - [Theoretical cost optimization by Amazon ECS launch type: Fargate vs EC2](https://aws.amazon.com/blogs/containers/theoretical-cost-optimization-by-amazon-ecs-launch-type-fargate-vs-ec2/)
        - > For steady-state, predictable workload levels that use a higher proportion of the instance CPU and memory, EC2 can be a more cost-effective choice, as it is possible to simply select the instance type for which tasks can optimally use the available resources.
        - > For highly dynamic workloads where right-sizing and scaling EC2 infrastructure introduces the risks of under/over-provisioning, the flexibility in cost and operation provided by Fargate would be beneficial.
- CloudFormation, ASG and desired count
    - [ECS + CloudFormation without clobbering desired counts?](https://www.reddit.com/r/aws/comments/6pwxkv/ecs_cloudformation_without_clobbering_desired/)
        > I've run into this as well, the ECS services behave subtly different from the ASG scaling. In ASG if you don't set the DesiredCapacity (which isn't required) then CFN/ASG will happily keep the existing value. However the DesiredCount is required for ECS Services so CFN will honor what you've put in the template and happily reset your service back to what's in your template. Even if that means going from 20 instances to 1 in a heartbeat.
    - [How can I correctly update my Auto Scaling group when I update my CloudFormation stack?](https://aws.amazon.com/premiumsupport/knowledge-center/auto-scaling-group-rolling-updates/)
    - [Refreshing an Amazon ECS Container Instance Cluster With a New AMI](https://aws.amazon.com/blogs/compute/refreshing-an-amazon-ecs-container-instance-cluster-with-a-new-ami/)
- ECS Cluster utilization and Service utilization
    - CPU Units example: A t3.medium has 2 vCPUs so it would be 2 x 1024 = 2048 CPU units
    - https://docs.aws.amazon.com/AmazonECS/latest/developerguide/cloudwatch-metrics.html#cluster_reservation
    - https://aws.amazon.com/blogs/containers/how-amazon-ecs-manages-cpu-and-memory-resources/
- CDK
    - [aws_cdk.aws_ecs](https://docs.aws.amazon.com/cdk/api/latest/docs/aws-ecs-readme.html)
    - [aws_cdk.aws_ecs_patterns](https://docs.aws.amazon.com/cdk/api/latest/docs/aws-ecs-patterns-readme.html)
      This library provides higher-level Amazon ECS constructs which follow common architectural patterns. It contains:
       - Application Load Balanced Services
       - Network Load Balanced Services
       - Queue Processing Services
       - Scheduled Tasks (cron jobs)
- MLA
    - Amazon ECS Log File Locations https://docs.aws.amazon.com/AmazonECS/latest/developerguide/logs.html
    - Amazon ECS Container Agent Configuration https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-agent-config.html
    - Example container instance user data configuration scripts https://docs.aws.amazon.com/AmazonECS/latest/developerguide/example_user_data_scripts.html
- Amazon ECS-optimized AMIs
    - https://docs.aws.amazon.com/AmazonECS/latest/developerguideecs-optimized_AMI.html

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

---
## Fargate

- Fargate does not give same cpu capacity for each task.
    - Just be aware on Fargate you can get `c` or `m` series instances under the hood.
If doing fine grained perf testing dump out `/proc/cpuinfo`` on the task to see what CPU you really have on Fargate.

### Mapping Fargate cpu to EC2 instance type

For Fargate cpu size e.g., 16384
- Considering 1024 units are 1vCPU
- 16384/1024 = 16 vCPU
- which matches c7g.4xlarge


---
## Building Container images in containers

- For self-hosted GitHub runners, possilbe options:
    - Kaniko Containers on Fargate - [Building container images on Amazon ECS on AWS Fargate](https://aws.amazon.com/blogs/containers/building-container-images-on-amazon-ecs-on-aws-fargate/), AWS, 2021-03-31
    - Use AWS Codebuild to build the container as a step https://github.com/aws-actions/aws-codebuild-run-build


---
## ECS - ENI trunking

([Source](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/container-instance-eni.html))

ℹ️ This feature is not available on Fargate.

Each ECS task that uses the `awsvpc` network mode receives its own ENI, which is attached to the container instance that hosts it. There is a default limit to the number of network interfaces that can be attached to an EC2 instance, and the primary network interface counts as one.

ECS supports launching container instances with increased ENI density using supported EC2 instance types. When you use these instance types and opt in to the `awsvpcTrunking` account setting, additional ENIs are available on newly launched container instances. This configuration allows you to place more tasks using the `awsvpc` network mode on each container instance.

### Example: c5.large instance

- By default, a c5.large instance may have up to `3` ENIs attached to it.
    - The primary network interface for the instance counts as `1`.
    - Each task using the `awsvpc` network mode requires an ENI, you can typically only run `2` such tasks on this instance type.
- With `awsvpcTrunking` enabled, a c5.large instance has an increased ENI limit of `12`.
    - The container instance will have the primary network interface\, and
    - ECS creates and attaches a "trunk" network interface to the container instance,
    - So this configuration allows you to launch `10` tasks on the container instance instead of the current `2` tasks.

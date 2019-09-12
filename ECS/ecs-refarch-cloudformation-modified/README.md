# ECS templates

ECS templates are modified based on https://github.com/aws-samples/ecs-refarch-cloudformation.

1. [ECS-VPV.template](ECS-VPC.template)

    Deploy a VPC, with a pair of public and private subnets spread across two
    Availability Zones. It deploys an Internet Gateway, with a default route on
    the public subnets. It deploys a pair of NAT Gateways (one in each AZ), and
    default routes for them in the private subnets.

1. [aws-quickstart.s3.amazonaws.com/quickstart-linux-bastion/templates/linux-bastion.template](
https://aws-quickstart.s3.amazonaws.com/quickstart-linux-bastion/templates/linux-bastion.template)

    Deploy a SSH bastion instance in the public subnets for connecting to container
    instances in private subnets.

1. [ECS-LoadBalancer.template](ECS-LoadBalancer.template)

    Deploy an Application Load Balancer that exposes our various ECS services.
    We create them it a separate nested template, so it can be referenced by
    all of the other nested templates.

1. [ECS-Cluster.template](ECS-Cluster.template)

    Deploy an ECS cluster to the provided VPC and subnets using an Auto Scaling Group.
    - Set up and initialise EC2 environment with CloudWatch `awslogs` enabled. 
    - Termination policies are set to ["OldestInstance", "OldestLaunchConfiguration"] - listed in the order in which
      they should apply).
    - Auto Scaling Scheduled Actions for terminating old ECS instance and start new ECS instance regularly
        - Scale down to 1 in Saturday morning
        - Scale up to 2 in Monday morning
    - Set up SNS (Email) Notification to notify ECS Auto Scaling Group activities
       - `autoscaling:EC2_INSTANCE_LAUNCH`
       - `autoscaling:EC2_INSTANCE_LAUNCH_ERROR`
       - `autoscaling:EC2_INSTANCE_TERMINATE`
       - `autoscaling:EC2_INSTANCE_TERMINATE_ERROR`
            
1. [ECS-ServiceBase.template](ECS-ServiceBase.template)

    Create CloudWatchLogsGroup, Role policies to be shared by multiple Tasks
    (Definitions). 

1. [ECS-LifecycleHook.template](ECS-LifecycleHook.template)

    Deploy a Lambda Function and Auto Scaling Lifecycle Hook to drain Tasks
    from your Container Instances when an Instance is selected for Termination
    in your Auto Scaling Group.

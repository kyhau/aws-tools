# Bottlerocket Notes

Jump to
- [Useful Libs and Tools](#useful-libs-and-tools)
- [Useful Articles and Blogs](#useful-articles-and-blogs)

---
## Useful Libs and Tools

- Update Bottlerocket https://github.com/bottlerocket-os/bottlerocket#updates
- ECS
    - [ECS-optimized Bottlerocket AMIs](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-bottlerocket.html)
    - [bottlerocket-ecs-updater](https://github.com/bottlerocket-os/bottlerocket-ecs-updater) - Bottlerocket ECS Updater is a service you can install into your ECS cluster that helps you keep your Bottlerocket container instances up to date.
    - [adamjkeller/bottlerocket-ecs-updater-cdk](https://github.com/adamjkeller/bottlerocket-ecs-updater-cdk) - deploy a demo container to Amazon ECS using Bottlerocket OS for the compute. In addition, a construct was created for the Bottlerocket updater based off of the CFN template required to deploy it.
- EKS
    - [EKS-optimized Bottlerocket AMIs](https://docs.aws.amazon.com/eks/latest/userguide/eks-optimized-ami-bottlerocket.html)
    - [bottlerocket-update-operator](https://github.com/bottlerocket-os/bottlerocket-update-operator) - Bottlerocket update operator is a Kubernetes operator that coordinates Bottlerocket updates on hosts in a cluster.
    - [aws-samples/amazon-eks-bottlerocket-nodes-on-graviton2](https://github.com/aws-samples/amazon-eks-bottlerocket-nodes-on-graviton2) - deploy a EKS cluster composed of two Managed Node Groups, one configured with x86-based and the other with Graviton2-based EC2 instance type, both of which utilize Bottlerocket-based AMI.

---
## Useful Articles and Blogs
- [Using a Bottlerocket AMI with Amazon ECS](https://github.com/bottlerocket-os/bottlerocket/blob/develop/QUICKSTART-ECS.md)

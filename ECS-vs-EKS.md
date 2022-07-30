# ECS vs. EKS

Jump to
- [What are ECS and EKS](#what-are-ecs-and-eks)
- [Simplicity vs. Flexibility](#simplicity-vs-flexibility)
- [Load Balancing](#load-balancing)
- [VPC and ENI](#vpc-and-eni)
- [ECS notes](./ECS/README.md)
- [EKS notes](./EKS/README.md)

---
## What are ECS and EKS

- ECS is a fully managed container orchestration service designed by AWS for Docker containers. It allows you to easily deploy, manage, and scale containerized applications on AWS.
- EKS is a fully managed container orchestration service designed by AWS for Kubernetes applications. It allows you to run Kubernetes on AWS without installing, operating, or maintaining a control plane or nodes.

ℹ️ Docker is a containerization platform and runtime.

ℹ️ Kubernetes is a platform for running and managing containers from many container runtimes. Kubernetes supports numerous container runtimes, including Docker.


---
## Simplicity vs. Flexibility

### ECS
- ECS is a native AWS solution, so it does not require a control pane.
- ECS has a simple API to create containerized applications without dealing with complex abstractions.
- ECS seamlessly integrates with other AWS services, e.g. ALB, NLB, IAM, CloudWatch, etc.
- Auto scaling (in-built managed scaling)
    - Target tracking scaling policies
    - Step scaling policies
    - Scheduled Scaling
- Security
    - ECS integrates with AWS IAM and ensures the containerized microservices or workloads are secure.
    - You can assign granular permissions for your tasks or containers, offering a high level of isolation.
    - ECS also integrates with other security and governance tools you trust to get to production quickly and securely.

### EKS
- EKS automatically manages the scalability and availability of the control plane nodes. These nodes are responsible for scheduling containers, storing cluster data, and other key tasks.
- EKS may rely more on native Kubernetes tooling and add-ons to manage configurations (e.g. `kubectl`, `helm`), such as the ones that govern users and roles (RBAC Mapping).
- Kubernetes is known for its vibrant ecosystem, consistent open-source APIs, and immense flexibility to customize application deployments with EKS and control how they operate.
- Auto scaling
    - EKS does not offer a fully managed scaling option. You need to manually configure requests, limits, and node-based or pod-based scaling to keep the use of resources in check.
    - Node-based autoscaling: Cluster Autoscaler, Karpenter
    - Pod-based autoscaling: Horizontal Pod Autoscaler, Vertical Pod Autoscaler
- Security
    - EKS needs EKS add-ons to enable AWS functionalities (e.g. IAM, Secrets Manager).
    - EKS also offers access to Kubernetes' native security tooling that allows admins and developers can benefit from. E.g., admins can analyze Kubernetes audit logs to investigate and identify security vulnerabilities or incidents (RBAC).

See also
- [ECS/README](./ECS/README.md)
- [EKS/README](./EKS/README.md)
- [Amazon ECS vs. EKS: Which Container Service to Choose in 2022?](https://www.simform.com/blog/amazon-ecs-vs-eks/)


---
## Load Balancing

![LoadBalancing-Diagram](https://miro.medium.com/max/700/0*iMPJ-d8_-sJwIAqn.png)

(Diagram [source](https://medium.com/swlh/eks-vs-ecs-orchestrating-containers-on-aws-9d49d3ff7f8d))

### EKS flow
1. The client sends a request to ELB.
2. ELB distributes the request to one of the nodes (aka EC2 instances).
3. A proxy running on the node is forwarding the request to one of the pods providing the service.

### ECS flow
1. The client sends a request to the ALB.
2. ALB forwards request to one of the tasks providing the service.

The proxy running on each node is distributing requests randomly or based on the round robin algorithm among all pods running in the cluster. Doing so increases the network traffic between EC2 instances and between AZs which consumes network capacity and adds latency.

In contrast, the tight integration between ECS and ALB does not require a third routing step and is, therefore, more efficient.


---
## VPC and ENI

![ENI-Diagram](https://miro.medium.com/max/700/0*KlCElQoKiuMOw8uw.png)

(Diagram [source](https://medium.com/swlh/eks-vs-ecs-orchestrating-containers-on-aws-9d49d3ff7f8d))

An argument for EKS is that it can support a much higher number of running pods (containers) per EC2 worker than ECS.
This is due to the way it uses ENIs.

### ECS - Each task is linked to a separate ENI
- ECS assigns each task (a group of containers) a separate ENI.
- You can assign an ENI directly to a task in EC2 using the `awsvpc` network mode. The task has its own IP address and the same networking properties as EC2 instances.
- With certain certain EC2 instance types (e.g. c5.18xlarge), the instance can support up to `120` tasks with `awsvpcTrunking` enabled. (See also [Elastic network interface trunking](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/container-instance-eni.html))

### EKS - Multiple tasks share the same ENI
- EKS assigns each pod (a group of containers) a private IP address.
- Multiple private IP addresses are assigned to each ENI. (See [Available IP Per ENI](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-eni.html#AvailableIpPerENI))
- Therefore EKS shares ENIs between pods.
- With certain EC2 instance type (e.g. c5.18xlarge), the instance can have 15 ENIs with 50 IPv4 addresses per ENI (i.e. 750 IP addresses). Therefore this will limit the true number of pods you can run per instance to `750`.

Note: Sharing ENIs between instances comes with a limitation - you are not able to restrict traffic with a security group per pod, as the ENI and therefore the security group is shared with multiple pods.

See also
- ENI trunking in [ECS/README](./ECS/README.md)
- [Amazon ECS vs EKS: Which Service is Right for You](https://www.missioncloud.com/blog/amazon-ecs-vs-eks-which-service-is-right-for-you)

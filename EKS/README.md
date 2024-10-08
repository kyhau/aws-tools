# EKS and AWS Controllers for Kubernetes

Jump to
- [AWS EKS, AWS Controllers for Kubernetes and related tools and libs](#aws-eks-aws-controllers-for-kubernetes-and-related-tools-and-libs)
- [Kubernetes tools (non-AWS)](#kubernetes-tools-non-aws)
- [QuickStart](#quick-start)
- [Networking](#networking)
- [AWS Secrets Manager and Kubernetes Secrets](#aws-secrets-manager-and-kubernetes-secrets)
- [Node-based autoscaling](#node-based-autoscaling)
    - Cluster Autoscaler
    - Karpenter
- [Pod-based autoscaling](#pod-based-autoscaling)
    - Horizontal Pod Autoscaler
    - Vertical Pod Autoscaler
- [EKS Montoring, Logging, Alerting](#eks-montoring-logging-alerting)
- [EKS cluster endpoint](#eks-cluster-endpoint)
- [EKS access control](#eks-access-control)
- [EKS security](#eks-security)
- [EKS IAM OIDC Provider](#eks-iam-oidc-provider)
- [EKS with Fargate](#eks-with-fargate)
- [Stress test](#stress-test)
- [CDK EKS+K8s Examples](#cdk-eksk8s-examples)
- [CDK / CDK8s Gotchas](#cdk--cdk8s-gotchas)

---
## AWS EKS, AWS Controllers for Kubernetes and related tools and libs

- CDK
    - [cdk8s](https://github.com/cdk8s-team/cdk8s) - Core library
    - [cdk8s-cli](https://github.com/cdk8s-team/cdk8s-cli) - Command-Line interface
    - [cdk8s-plus](https://github.com/cdk8s-team/cdk8s-plus) - (cdk8s+ or cdk8s-plus) High-Level constructs for Kubernetes core
    - [Examples](#cdk-eksk8s-examples) - cdk / cdk8s / k8s
    - [Gotchas](#cdk--cdk8s-gotchas) - cdk / cdk8s
- CLIs
    - [eksctl](https://github.com/weaveworks/eksctl) - CLI tool for creating EKS clusters
- EKS Blueprints
    - [Bootstrapping clusters with EKS Blueprints](https://aws.amazon.com/blogs/containers/bootstrapping-clusters-with-eks-blueprints/)
    - [App2Container Support for EKS Blueprints](https://aws.amazon.com/about-aws/whats-new/2022/11/app2container-support-eks-blueprints/)
- EKS Charts (Helm)
    - [eks-charts](https://github.com/aws/eks-charts) - AWS EKS Charts (Helm)
- EKS Distro
    - [eks-distro](https://github.com/aws/eks-distro) - EKS Distro (EKS-D) is a Kubernetes distribution based on and used by EKS to create Kubernetes clusters
    - EKS Distro in [ECR Public Gallery](https://gallery.ecr.aws/?searchTerm=EKS+Distro)
- Controllers
    - [aws-controllers-k8s](https://github.com/aws/aws-controllers-k8s/) - AWS Controllers for Kubernetes (ACK), e.g. eks-controller, ec2-controller, s3-controller, apigatewayv2-controller, lambda-controller
    - [aws-controllers-k8s/test-infra](https://github.com/aws-controllers-k8s/test-infra) - This repository contains a framework for functional integration (e2e) testing of AWS Controllers for Kubernetes (ACK) service controllers.
    - [aws-eks-cluster-controller](https://github.com/awslabs/aws-eks-cluster-controller) - AWS EKS Cluster Controller
    - [zone-aware-controllers-for-k8s](https://github.com/aws/zone-aware-controllers-for-k8s) - Kubernetes controllers for zone (AZ) aware rollouts and disruptions.
- Kubectl Handler
   - KubectlHandler cab be used to restrict calling `kubebtl` / `helm` commands within a VPC-hosted Lambda function. See https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_eks-readme.html.
     > The kubectl handler uses kubectl, helm and the aws CLI in order to interact with the cluster. These are bundled into AWS Lambda layers included in the @aws-cdk/lambda-layer-awscli and @aws-cdk/lambda-layer-kubectl modules.
- Access control, security, hardening
    - [aws-iam-authenticator](https://github.com/kubernetes-sigs/aws-iam-authenticator) - AWS IAM Authenticator for Kubernetes,
    [how-to-install](https://docs.aws.amazon.com/eks/latest/userguide/install-aws-iam-authenticator.html)
    - [Amazon Detective adds Amazon VPC Flow Logs visualizations for Amazon EKS workloads](https://aws.amazon.com/about-aws/whats-new/2023/01/amazon-detective-vpc-flow-logs-visualizations-eks-workloads/)
    - [Amazon GuardDuty for EKS Protection](https://aws.amazon.com/about-aws/whats-new/2022/01/amazon-guardduty-elastic-kubernetes-service-clusters/)
    - [hardeneks](https://github.com/aws-samples/hardeneks) - Hardeneks runs checks to see if an EKS cluster follows [EKS Best Practices](https://aws.github.io/aws-eks-best-practices/).
- Maintenance
    - [aws-node-termination-handler](https://github.com/aws/aws-node-termination-handler) - AWS Node Termination Handler (NTH) - Gracefully handle EC2 instance shutdown within Kubernetes
    - [deploy-nth-to-eks](https://github.com/aws-samples/deploy-nth-to-eks) - Automate Deployment of Node Termination Handler (NTH) in Self Managed Worker Node in EKS Cluster using CICD Pipeline
- MLTA
    - [eks-event-watcher](https://github.com/aws-samples/eks-event-watcher) - EKS (control plane) event watcher
    - [eks-node-viewer](https://github.com/awslabs/eks-node-viewer) - a tool for visualizing dynamic node usage within a cluster. It was originally developed as an internal tool at AWS for demonstrating consolidation with Karpenter.
    - [aws-observability/aws-otel-collector](https://github.com/aws-observability/aws-otel-collector) - AWS Distro for OpenTelemetry Collector
    - [aws-observability/aws-otel-helm-charts](https://github.com/aws-observability/aws-otel-helm-charts) -  AWS Distro for OpenTelemetry (ADOT) Helm Charts
    - [aws-observability/amp-eks-iam](https://github.com/aws-observability/amp-eks-iam) - Tool providing easy IAM setup on EKS for Amazon Managed Service for Prometheus (AMP) users.
    - [aws-observability/amp-k8s-config-examples](https://github.com/aws-observability/amp-k8s-config-examples) - Configurations for Prometheus including Kubernetes (k8s) Helm charts and Operators
- Networking
    - [amazon-vpc-cni-k8s](https://github.com/aws/amazon-vpc-cni-k8s) - Networking plugin for pod networking in Kubernetes using ENIs on AWS.
    - Calico add-on - network policy engine for Kubernetes
       - https://docs.aws.amazon.com/eks/latest/userguide/calico.html
- Persistent storage [doc](https://aws.amazon.com/premiumsupport/knowledge-center/eks-persistent-storage/)
    - [aws-ebs-csi-driver](https://github.com/kubernetes-sigs/aws-ebs-csi-driver) - AWS EBS CSI Driver on Kubernetes
    - [aws-efs-csi-driver](https://github.com/kubernetes-sigs/aws-efs-csi-driver) - AWS EFS CSI Driver on Kubernetes
    - Using Amazon EBS snapshots for persistent storage with your Amazon EKS cluster by leveraging add-ons ([blog post](https://aws.amazon.com/blogs/containers/using-amazon-ebs-snapshots-for-persistent-storage-with-your-amazon-eks-cluster-by-leveraging-add-ons/))
- Scaling
    - [aws-karpenter](https://github.com/aws/karpenter) - AWS Karpenter
- Testing
    - [aws-k8s-tester](https://github.com/aws/aws-k8s-tester) - is a set of utilities and libraries for "testing" Kubernetes on AWS.
    - AWS FIS (Fault Injection Simulator) with [ChaosMesh and Litmus support](https://aws.amazon.com/about-aws/whats-new/2022/07/aws-fault-injection-simulator-supports-chaosmesh-litmus-experiments/) for stress testing EKS
- Upgrade
    - [eksupgrade](https://github.com/aws-samples/eks-cluster-upgrade) - Amazon EKS Upgrade Utility

---
## Kubernetes tools (non-AWS)

- [kyhau/workspace/useful-tools/kubernetes](https://github.com/kyhau/workspace/tree/main/useful-tools/kubernetes)


## Best Practices Guides

- [Making sense of secrets management on Amazon EKS for regulated institutions](https://aws.amazon.com/blogs/security/making-sense-of-secrets-management-on-amazon-eks-for-regulated-institutions/), AWS, 2024-08-19
- [Amazon EKS Best Practices Guide for Security](https://aws.github.io/aws-eks-best-practices/), AWS


## Quick Start

- EKS Kubernetes [versions and release calendar](https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions.html#kubernetes-release-calendar)
- ALB Controller - https://docs.aws.amazon.com/eks/latest/userguide/aws-load-balancer-controller.html
- ALB Ingress - https://docs.aws.amazon.com/eks/latest/userguide/alb-ingress.html
- https
    - AWS ALB Ingress Service - Enable SSL - https://www.stacksimplify.com/aws-eks/aws-alb-ingress/learn-to-enable-ssl-on-alb-ingress-service-in-kubernetes-on-aws-eks/
    - Setting up end-to-end TLS encryption on Amazon EKS with the new AWS Load Balancer Controller - https://aws.amazon.com/blogs/containers/setting-up-end-to-end-tls-encryption-on-amazon-eks-with-the-new-aws-load-balancer-controller/)
- Cluster Autoscaler
    - NEW - [Karpenter](https://github.com/aws/karpenter)
    - Parameters supported for cluster autoscaler - https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/FAQ.md#what-are-the-parameters-to-ca
    - https://docs.cloudbees.com/docs/cloudbees-ci/latest/cloud-admin-guide/eks-auto-scaling-nodes
- Kubernetes Dashboard https://github.com/kubernetes/dashboard
- Metrics Server and Metrics API - https://www.datadoghq.com/blog/how-to-collect-and-graph-kubernetes-metrics/
- [kube-bench](https://github.com/aquasecurity/kube-bench) is a tool that checks whether Kubernetes is deployed securely by running the checks documented in the CIS Kubernetes Benchmark. https://github.com/aquasecurity/kube-bench
- EKS Best Practices https://aws.github.io/aws-eks-best-practices/
- EKS Workshop https://www.eksworkshop.com


## Networking

### Max number of pods per EC2 instance

- With certain EC2 instance type (e.g. m5.24xlarge), the instance can have 15 ENIs with 50 ipv4 addresses per ENI. (See [Available IP Per ENI](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-eni.html#AvailableIpPerENI))
- This will give you 750 IP addresses per host, and thus will limit the true number of pods you can run per host to 750.

### Amazon VPC CNI plugin for K8s
- [amazon-vpc-cni-k8s](https://github.com/aws/amazon-vpc-cni-k8s) - Networking plugin for pod networking in Kubernetes using ENIs on AWS.

### Calico add-on - network policy engine for Kubernetes
- https://docs.aws.amazon.com/eks/latest/userguide/calico.html


## AWS Secrets Manager and Kubernetes Secrets

- [External Secrets provider - AWS Secrets Manager](https://external-secrets.io/provider-aws-secrets-manager/)
- [Managing Kubernetes Secrets with AWS Secrets Manager](https://thenewstack.io/managing-kubernetes-secrets-with-aws-secrets-manager/), Janakiram MSV, 19 Jul 2021
- [kubernetes-external-secrets](https://github.com/external-secrets/kubernetes-external-secrets) (Deprecated) but README is useful (AWS Secrets Manager, dataFrom)


## Node-based autoscaling
Adding or removing nodes as needed
- [Cluster Autoscaler](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler)
- [Karpenter](https://karpenter.sh/docs/getting-started/)
   - https://github.com/aws/karpenter
   - [aws-samples/cdk-eks-karpenter](https://github.com/aws-samples/cdk-eks-karpenter)

### Cluster Autoscaler vs. Karpenter
- https://kubesandclouds.com/index.php/2022/01/04/karpenter-vs-cluster-autoscaler/
- https://towardsdev.com/karpenter-vs-cluster-autoscaler-dd877b91629b

### Karpenter improvements ([Source](https://kubesandclouds.com/index.php/2022/01/04/karpenter-vs-cluster-autoscaler/))
- Designed to handle the full flexibility of the cloud: Karpenter has the ability to efficiently address the full range of instance types available through AWS. Cluster autoscaler was not originally built with the flexibility to handle hundreds of instance types, zones, and purchase options.
- Group-less node provisioning: Karpenter manages each instance directly, without using additional orchestration mechanisms like node groups. This enables it to retry in milliseconds instead of minutes when capacity is unavailable. It also allows Karpenter to leverage diverse instance types, availability zones, and purchase options without the creation of hundreds of node groups.
- Scheduling enforcement: Cluster autoscaler doesn’t bind pods to the nodes it creates. Instead, it relies on the kube-scheduler to make the same scheduling decision after the node has come online. A node that Karpenter launches has its pods bound immediately. The kubelet doesn’t have to wait for the scheduler or for the node to become ready. It can start preparing the container runtime immediately, including pre-pulling the image. This can shave seconds off of node startup latency.
- [Workload Consolidation for Karpenter](https://aws.amazon.com/about-aws/whats-new/2022/08/workload-consolidation-karpenter/): Workload consolidation for Karpenter automatically looks for opportunities to reschedule these workloads onto a set of more cost-efficient EC2 instances, whether they are already in the cluster or need to be launched.


## Pod-based autoscaling

1. [Horizontal Pod Autoscaler](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/) – add or remove more pods to the deployment as needed
2. [Vertical Pod Autoscaler](https://cloud.google.com/kubernetes-engine/docs/concepts/verticalpodautoscaler) – resize pod's CPU and memory requests and limits to match the load

Autoscaling EKS on Fargate
1. [Autoscaling EKS on Fargate with custom metrics](https://aws.amazon.com/blogs/containers/autoscaling-eks-on-fargate-with-custom-metrics/) with HorizontalPodAutoscaler
   - Examples of configuring autoscaling based on HTTP traffic, CPU and/or memory usage, App Mesh traffic


## EKS Montoring, Logging, Alerting

- [Logging for Amazon EKS](https://docs.aws.amazon.com/prescriptive-guidance/latest/implementing-logging-monitoring-cloudwatch/kubernetes-eks-logging.html)
    - Amazon EKS control plane logging
        - [Enable EKS control plane logging](https://docs.aws.amazon.com/eks/latest/userguide/control-plane-logs.html)
    - Amazon EKS node and application logging
    - Logging for Amazon EKS on Fargate
        - [CloudWatch Container Insights adds support for EKS Fargate using AWS Distro for OpenTelemetry](https://aws.amazon.com/about-aws/whats-new/2022/02/amazon-cloudwatch-eks-fargate-distro-opentelemetry/)
- [Send logs to CloudWatch Logs with Fluent Bit or Fluentd](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Container-Insights-EKS-logs.html)
- [Setting up Container Insights on Amazon EKS and Kubernetes](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/deploy-container-insights-EKS.html)
- Metrics and Alarms
    - [EKS and Kubernetes Container Insights metrics list](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Container-Insights-metrics-EKS.html)
    - [Relevant fields in performance log events for Amazon EKS and Kubernetes](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Container-Insights-reference-performance-entries-EKS.html)
    - [CloudWatch metrics to generate various alarms for your EKS Cluster based on assigned metrics](https://www.eksworkshop.com/intermediate/250_cloudwatch_container_insights/cwalarms/)
- See also
    - [Kubernetes Alerting | Best Practices in 2022](https://www.containiq.com/post/kubernetes-alerting-best-practices)


## EKS cluster endpoint

[EKS cluster endpoint access control](https://docs.aws.amazon.com/eks/latest/userguide/cluster-endpoint.html)

- Private access for EKS cluster's Kubernetes API server endpoint (Kubernetes control plane API)
    - A cluster that has been configured to only allow private access can only be accessed from the following: ([Source](https://aws.amazon.com/blogs/compute/enabling-dns-resolution-for-amazon-eks-cluster-endpoints/))
        - The VPC where the worker nodes reside.
        - Networks that have been peered with that VPC.
        - A network that has been connected to AWS through Direct Connect (DX) or a VPN.
    - However, the name of the Kubernetes cluster endpoint is only resolvable from the worker node VPC, for the following reasons:
        - The Route 53 private hosted zone that is created for the endpoint is only associated with the worker node VPC.
        - The private hosted zone is created in a separate AWS managed account and cannot be altered.
    - The cluster's API server endpoint is resolved by public DNS servers to a private IP address from the VPC. When you do a DNS query for your API server endpoint (e.g. `9FF86DB0668DC670F27F426024E7CDBD.sk1.us-east-1.eks.amazonaws.com`) it will return private IP of EKS Endpoint (e.g. 10.10.10.20).
        - However, `.gr7.ap-southeast-2.eks.amazonaws.com` is NOT unique to account or region.
            ```
            Account-1:
                ap-southeast-2:  https://FD743253263F9932A1C1359F134D9B08.gr7.ap-southeast-2.eks.amazonaws.com
                ap-southeast-1:  https://7296B66098508057814BDC28DD6442FE.gr7.ap-southeast-1.eks.amazonaws.com
            Account-2:
                ap-southeast-2:  https://0395CA66195A658536B531CA06F3246D.gr7.ap-southeast-2.eks.amazonaws.com
                ap-southeast-2:  https://C2D57012E496E6903F975147013EE156.sk1.ap-southeast-2.eks.amazonaws.com
            Account-3:
                us-east-1:       https://9FF86DB0668DC670F27F426024E7CDBD.sk1.us-east-1.eks.amazonaws.com
            ```
- How to enable private access for the EKS cluster's Kubernetes API server endpoint?
    1. Update `Cluster.endpointAccess` to `PRIVATE`.
    1. Create or update your “Security Group to use for Control Plane ENIs” with the ingress rules for your client (e.g. `kubectl`) to access the Kubernetes control plane API from the deployment agents (e.g. GitHub Actions Workflow)
        - In CloudFormation, it is a Security Group in [ResourcesVpcConfig.SecurityGroupIds](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-resourcesvpcconfig.html).
        - In CDK, it is securityGroup in [aws-cdk-lib.aws_eks.Cluster](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_eks.Cluster.html) `ClusterProps`.
    1. If your deployment agent is in another VPC / AWS account, then you will need a solution for directing the DNS request to the corresponding VPC / account.
- How do I lock down API access to specific IP addresses in my Amazon EKS cluster?
    - You can, optionally, limit the CIDR blocks that can access the public endpoint. If you limit access to specific CIDR blocks, then it is recommended that you also enable the private endpoint, or ensure that the CIDR blocks that you specify include the addresses that nodes and Fargate pods (if you use them) access the public endpoint from.
    1. Update `Cluster.endpointAccess` to `PUBLIC_AND_PRIVATE`.
        - In CloudFormation, add the CIDR to `ResourcesVpcConfig.PublicAccessCidrs`.
        - In CDK, add the CIDR to `endpointAccess: EndpointAccess.PUBLIC_AND_PRIVATE.onlyFrom(...)` in [aws-cdk-lib.aws_eks.Cluster](https://github.com/aws/aws-cdk/blob/master/packages/%40aws-cdk/aws-eks/lib/cluster.ts) `ClusterProps`.
    - See [How do I lock down API access to specific IP addresses in my Amazon EKS cluster?](https://aws.amazon.com/premiumsupport/knowledge-center/eks-lock-api-access-IP-addresses/)
    - See [Amazon EKS cluster endpoint access control](https://docs.aws.amazon.com/eks/latest/userguide/cluster-endpoint.html)
- DNS resolution for EKS cluster endpoints
    - [Enabling DNS resolution for Amazon EKS cluster endpoints](https://aws.amazon.com/blogs/compute/enabling-dns-resolution-for-amazon-eks-cluster-endpoints/)
    - [DNS Resolution for EKS Clusters Using Private Endpoints](https://aws.amazon.com/about-aws/whats-new/2019/12/dns-resolution-for-eks-clusters-using-private-endpoints/)
    - [Understanding Amazon EKS Cluster Private Endpoint Access](https://faun.pub/understanding-amazon-eks-cluster-private-endpoint-access-76ca52bf978a)


## EKS access control

- [eks-pod-identity-agent](https://github.com/aws/eks-pod-identity-agent) - Amazon EKS Pod Identity agent
- IRSA vs. Pod Identity
    - [New attack vectors in EKS](https://www.wiz.io/blog/new-attack-vectors-emerge-via-recent-eks-access-entries-and-pod-identity-features), Wiz, 2024-02-10
- [How do I provide access to other IAM users and roles after cluster creation in Amazon EKS?](https://aws.amazon.com/premiumsupport/knowledge-center/amazon-eks-cluster-access/)
    -  Important: Keep the following in mind:
        - Avoid syntax errors (such as typos) when you update the `aws-auth` ConfigMap. These errors can affect the permissions of all IAM users and roles updated within the ConfigMap of the Amazon EKS cluster.
        - It's a best practice to avoid adding `cluster_creator` to the ConfigMap, because improperly modifying the ConfigMap can cause all IAM users and roles (including `cluster_creator`) to permanently lose access to the Amazon EKS cluster.
        - You don't need to add `cluster_creator` to the `aws-auth` ConfigMap to get admin access to the Amazon EKS cluster. By default, the `cluster_creator` has admin access to the Amazon EKS cluster that it created.
- [Manage Amazon EKS with Okta SSO](https://aws.amazon.com/blogs/containers/manage-amazon-eks-with-okta-sso/)
    - > EKS uses IAM to provide authentication to your Kubernetes cluster, but it still relies on native Kubernetes Role-Based Access Control (RBAC) for authorization. This means that IAM is only used for authentication of valid IAM entities. All permissions for interacting with your Amazon EKS cluster’s Kubernetes API is managed through the native Kubernetes RBAC system.
    - https://github.com/aws-samples/eks-rbac-sso



## EKS security

- [Making sense of secrets management on Amazon EKS for regulated institutions](https://aws.amazon.com/blogs/security/making-sense-of-secrets-management-on-amazon-eks-for-regulated-institutions/), AWS, 2024-08-19
- [Amazon EKS Best Practices Guide for Security](https://aws.github.io/aws-eks-best-practices/), AWS
- [Configure mutual TLS authentication for applications running on Amazon EKS](https://docs.aws.amazon.com/prescriptive-guidance/latest/patterns/configure-mutual-tls-authentication-for-applications-running-on-amazon-eks.html) with NLB
- [Amazon Detective Supports Kubernetes Workloads on Amazon EKS for Security Investigations](https://aws.amazon.com/blogs/aws/amazon-detective-supports-kubernetes-workloads-on-amazon-eks-for-security-investigations/)
- [Amazon GuardDuty protects Amazon Elastic Kubernetes Service clusters](https://aws.amazon.com/about-aws/whats-new/2022/01/amazon-guardduty-elastic-kubernetes-service-clusters/)


## EKS IAM OIDC Provider

1. `iam:*OpenIDConnectProvider*` permissions are not required when creating an EKS cluster with `CreateCluster`, which creates an **OpenID Connect provider URL** (OpenID Connect issuer URL) for the cluster (e.g. https://oidc.eks.ap-southeast-2.amazonaws.com/id/ABCABC111222333444ABCABC11122233).
    - And in CloudTrail, there are no `*OpenIDConnectProvider*` events.

2.  After (1), the cluster has an OpenID Connect issuer URL associated with it.  To use IAM roles for service accounts, an IAM OIDC provider must exist for the cluster. See [here](https://docs.aws.amazon.com/eks/latest/userguide/enable-iam-roles-for-service-accounts.html).
You need to run `ekctl utils associate-iam-oidc-provider`,
    ```
    $ eksctl utils associate-iam-oidc-provider --cluster=k-test-oicd --approve --region=ap-southeast-2 --profile test-oidc
    ```
    - A **Open ID Provider** with the same URL as (1) is created.
    - For this step, this role needs to have the following permissions
        ```
        iam:CreateOpenIDConnectProvider
        iam:GetOpenIDConnectProvider
        iam:TagOpenIDConnectProvider
        ```
    - CloudTrail does NOT show the events as well (e.g. `CreateOpenIDConnectProvider`)


## EKS with Fargate

There are some potential drawbacks to using Fargate with EKS, both operational and for workload security. ([Source](https://www.stackrox.io/blog/securing-eks-cluster-add-ons-dashboard-fargate-ec2-components-and-more/))

1. Kubernetes network policies silently have no effect on pods assigned to Fargate nodes. Daemon sets, which put a pod for a service on each node, cannot place pods on the Fargate virtual nodes. Even if Calico could run as a sidecar in a pod, it would not have permission to manage the pod’s routing, which requires root privileges. Fargate only allows unprivileged containers.
2. Active security monitoring of a container’s actions on Fargate becomes difficult or nearly impossible.
3. Any metrics or log collectors that a user may normally run as a cluster daemon set will also have to be converted to sidecars, if possible.
4. EKS still requires clusters that use Fargate for all their pod scheduling to have at least one node.
5. The exact security implications and vulnerabilities of running EKS pods on Fargate remain unknown for now.

See also [AWS Fargate considerations](https://docs.aws.amazon.com/eks/latest/userguide/fargate.html#fargate-considerations).


## Stress test

- AWS FIS (Fault Injection Simulator)
   - FIS supports [ChaosMesh and Litmus](https://aws.amazon.com/about-aws/whats-new/2022/07/aws-fault-injection-simulator-supports-chaosmesh-litmus-experiments/) experiments for containerized applications running on EKS.
     > E.g. run a stress test on a pod’s CPU using ChaosMesh or Litmus faults while terminating a randomly selected percentage of cluster nodes using FIS fault actions.


## CDK EKS+K8s Examples

- [aws-samples/amazon-eks-using-cdk-typescript](https://github.com/aws-samples/amazon-eks-using-cdk-typescript) - A sample project that deploys an EKS Cluster following a set of best practices with options to install additional addons. Easy deployment of the EBS CSI Driver, EFS CSI Driver, FluentBit Centralized Logging using Cloudwatch, Cluster Autoscaler, ALB Ingress Controller, Secrets CSI Driver and Network Policy Engine.
- [aws-samples/cdk-eks-fargate](https://github.com/aws-samples/cdk-eks-fargate) - leverage cdk, cdk8s and cdk8s+ to provision an ESK cluster with Fargate node groups, deploy workloads and expose Kubernetes services.
- [aws-samples/amazon-eks-cdk-blue-green-cicd](https://github.com/aws-samples/amazon-eks-cdk-blue-green-cicd) - Building CI/CD with Blue/Green and Canary Deployments on EKS using CDK
- [aws-samples/aws-cdk-pipelines-eks-cluster](https://github.com/aws-samples/aws-cdk-pipelines-eks-cluster) - CDK Pipelines for EKS Cluster(s)
- [aws-quickstart/quickstart-helm-resource-provider](https://github.com/aws-quickstart/quickstart-helm-resource-provider) - `AWSQS::Kubernetes::Helm` - An AWS CloudFormation resource provider for the management of helm 3 resources in EKS and self-managed Kubernetes clusters
- [aws-samples/aws-lambda-layer-kubectl](https://github.com/aws-samples/aws-lambda-layer-kubectl) - How to create your own Lambda layer with kubectl in CDK
- [aws-samples/cdk-eks-karpenter](https://github.com/aws-samples/cdk-eks-karpenter) - This construct configures the necessary dependencies and installs Karpenter on an EKS cluster managed by AWS CDK.


## cdk / cdk8s Gotchas

- [aws-cdk-lib.aws_eks.Cluster](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_eks.Cluster.html) supports specifying only one Security Group (but CloudFormation/Console support list of Security Groups).
- Currently there is no way to get FilterName using CDK, see [aws-cdk/issues/8141](https://github.com/aws/aws-cdk/issues/8141). Workaround: `const clusterSubFilterName = clusterSubFilter.stack.getLogicalId(clusterSubFilter.node.defaultChild as CfnSubscriptionFilter)`.

# EKS Notes

Jump to
- [EKS tools and libs](#eks-tools-and-libs)
- [Kubernetes tools (non-AWS)](#kubernetes-tools-non-aws)
- [QuickStart](#quick-start)
- [EKS Montoring, Logging, Alerting](#eks-montoring-logging-alerting)
- [EKS security and access control](#eks-security-and-access-control)
- [EKS IAM OIDC Provider](#eks-iam-oidc-provider)


---
## EKS tools and libs

- CDK
    - [cdk8s](https://github.com/cdk8s-team/cdk8s) - CDK for Kubernetes
    - [cdk8s-cli](https://github.com/cdk8s-team/cdk8s-cli) - CLI for CDK for Kubernetes
    - [cdk8s-plus](https://github.com/cdk8s-team/cdk8s-plus) - cdk8s+ (cdk8s-plus) is a software development framework that provides high level abstractions for authoring Kubernetes applications.
    - [aws-samples/amazon-eks-cdk-blue-green-cicd](https://github.com/aws-samples/amazon-eks-cdk-blue-green-cicd) - Building CI/CD with Blue/Green and Canary Deployments on EKS using CDK
    - [aws-samples/aws-cdk-pipelines-eks-cluster](https://github.com/aws-samples/aws-cdk-pipelines-eks-cluster) - CDK Pipelines for EKS Cluster(s)
    - Gotchas
        - [aws-cdk-lib.aws_eks.Cluster](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_eks.Cluster.html) supports specifying only one Security Group (but CloudFormation/Console support list of Security Groups).
- [eksctl](https://github.com/weaveworks/eksctl) - Official CLI for Amazon EKS
- [eks-distro](https://github.com/aws/eks-distro)
    - EKS Distro (EKS-D) is a Kubernetes distribution based on and used by EKS to create reliable and secure Kubernetes clusters.
    - [ECR Public Gallery](https://gallery.ecr.aws/?searchTerm=EKS+Distro)
- [kubectl (Amazon EKS-vended)](https://docs.aws.amazon.com/eks/latest/userguide/install-kubectl.html)
- [aws-iam-authenticator](https://github.com/kubernetes-sigs/aws-iam-authenticator) - AWS IAM Authenticator for Kubernetes,
[how-to-install](https://docs.aws.amazon.com/eks/latest/userguide/install-aws-iam-authenticator.html)
- [aws-controllers-k8s](https://github.com/aws/aws-controllers-k8s/) - AWS Controllers for Kubernetes (ACK)
- [karpenter](https://github.com/aws/karpenter) - AWS Karpenter - Kubernetes Cluster Autoscaler
- [aws-eks-cluster-controller](https://github.com/awslabs/aws-eks-cluster-controller) - AWS EKS Cluster Controller
- [aws-node-termination-handler](https://github.com/aws/aws-node-termination-handler) - AWS Node Termination Handler - Gracefully handle EC2 instance shutdown within Kubernetes
- [eks-charts](https://github.com/aws/eks-charts) - AWS EKS Charts (Helm)
- [EKS persistent storage](https://aws.amazon.com/premiumsupport/knowledge-center/eks-persistent-storage/)
    - [aws-ebs-csi-driver](https://github.com/kubernetes-sigs/aws-ebs-csi-driver) - AWS EBS CSI Driver on Kubernetes
    - [aws-efs-csi-driver](https://github.com/kubernetes-sigs/aws-efs-csi-driver) - AWS EFS CSI Driver on Kubernetes


---
## Kubernetes tools (non-AWS)

- [kyhau/workspace/useful-tools/kubernetes](https://github.com/kyhau/workspace/tree/main/useful-tools/kubernetes)


---
## Quick Start

- EKS Kubernetes [versions and release calendar](https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions.html#kubernetes-release-calendar)
- EKS Distro
    - https://gallery.ecr.aws/?searchTerm=EKS+Distro
    - https://github.com/aws/eks-distro
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
- AWSQS::Kubernetes::Helm https://github.com/aws-quickstart/quickstart-helm-resource-provider


---
## EKS Montoring, Logging, Alerting

- [Logging for Amazon EKS](https://docs.aws.amazon.com/prescriptive-guidance/latest/implementing-logging-monitoring-cloudwatch/kubernetes-eks-logging.html)
    - Amazon EKS control plane logging
        - [Enable EKS control plane logging](https://docs.aws.amazon.com/eks/latest/userguide/control-plane-logs.html)
    - Amazon EKS node and application logging
    - Logging for Amazon EKS on Fargate
        - [CloudWatch Container Insights adds support for EKS Fargate using AWS Distro for OpenTelemetry](https://aws.amazon.com/about-aws/whats-new/2022/02/amazon-cloudwatch-eks-fargate-distro-opentelemetry/)
- [Send logs to CloudWatch Logs with Fluent Bit or Fluentd](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Container-Insights-EKS-logs.html)
- [Setting up Container Insights on Amazon EKS and Kubernetes](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/deploy-container-insights-EKS.html)


---
## EKS security and access control

- [EKS cluster endpoint access control](https://docs.aws.amazon.com/eks/latest/userguide/cluster-endpoint.html)
    - [Enabling DNS resolution for Amazon EKS cluster endpoints](https://aws.amazon.com/blogs/compute/enabling-dns-resolution-for-amazon-eks-cluster-endpoints/)
    - [DNS Resolution for EKS Clusters Using Private Endpoints](https://aws.amazon.com/about-aws/whats-new/2019/12/dns-resolution-for-eks-clusters-using-private-endpoints/)
    - [Understanding Amazon EKS Cluster Private Endpoint Access](https://faun.pub/understanding-amazon-eks-cluster-private-endpoint-access-76ca52bf978a)
- [How do I provide access to other IAM users and roles after cluster creation in Amazon EKS?](https://aws.amazon.com/premiumsupport/knowledge-center/amazon-eks-cluster-access/)
    -  Important: Keep the following in mind:
        - Avoid syntax errors (such as typos) when you update the `aws-auth` ConfigMap. These errors can affect the permissions of all IAM users and roles updated within the ConfigMap of the Amazon EKS cluster.
        - It's a best practice to avoid adding `cluster_creator` to the ConfigMap, because improperly modifying the ConfigMap can cause all IAM users and roles (including `cluster_creator`) to permanently lose access to the Amazon EKS cluster.
        - You don't need to add `cluster_creator` to the `aws-auth` ConfigMap to get admin access to the Amazon EKS cluster. By default, the `cluster_creator` has admin access to the Amazon EKS cluster that it created.
- [Manage Amazon EKS with Okta SSO](https://aws.amazon.com/blogs/containers/manage-amazon-eks-with-okta-sso/)
    - > EKS uses IAM to provide authentication to your Kubernetes cluster, but it still relies on native Kubernetes Role-Based Access Control (RBAC) for authorization. This means that IAM is only used for authentication of valid IAM entities. All permissions for interacting with your Amazon EKS cluster’s Kubernetes API is managed through the native Kubernetes RBAC system.
    - https://github.com/aws-samples/eks-rbac-sso
    -

---
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

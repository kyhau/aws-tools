# EKS Notes

Jump to
- [Userful Libs and Tools](#useful-libs-and-tools)
- Non-AWS / Kubernetes tools: [kyhau/workspace/useful-tools/kubernetes](https://github.com/kyhau/workspace/tree/master/useful-tools/kubernetes)
- [QuickStart](#quick-start)
- [CDK for Kubernetes cdk8s / cdk8s+](#cdk-for-Kubernetes-cdk8s)
- [EKS IAM OIDC Provider](#eks-iam-oidc-provider)
- [EKS Persistent Storage](eks-persistent-storage)
- [EKS logging](#eks-logging)
- [Collecting metrics with built-in Kubernetes monitoring tools](#collecting-metrics-with-built-in-kubernetes-monitoring-tools)
- [Kubernetes Metrics Server](#kubernetes-metrics-server)

---
## Useful Libs and Tools

| EKS | Repo/Link |
| :--- | :--- |
| Amazon EKS CLI | [weaveworks/eksctl](https://github.com/weaveworks/eksctl) |
| Amazon EKS Distro (EKS-D) - a Kubernetes distribution based on and used by EKS to create reliable and secure Kubernetes clusters | [aws/eks-distro](https://github.com/aws/eks-distro), <br/> [ECR Public Gallery](https://gallery.ecr.aws/?searchTerm=EKS+Distro) |
| Amazon EKS-vended aws-iam-authenticator | [Amazon EKS-vended aws-iam-authenticator](https://docs.aws.amazon.com/eks/latest/userguide/install-aws-iam-authenticator.html) |
| Amazon EKS-vended kubectl | [Amazon EKS-vended kubectl](https://docs.aws.amazon.com/eks/latest/userguide/install-kubectl.html) |
| AWS cdk8s - [CDK for Kubernetes](https://cdk8s.io/) | [cdk8s-team/cdk8s](https://github.com/cdk8s-team/cdk8s) |
| AWS cdk8s-cli - a CLI for CDK for Kubernetes | [cdk8s-team/cdk8s-cli](https://github.com/cdk8s-team/cdk8s-cli) |
| AWS cdk8s-plus | [cdk8s-team/cdk8s-plus](https://github.com/cdk8s-team/cdk8s-plus) |
| AWS Controllers for Kubernetes (ACK) | [aws/aws-controllers-k8s](https://github.com/aws/aws-controllers-k8s/) |
| AWS EKS Cluster Controller | [awslabs/aws-eks-cluster-controller](https://github.com/awslabs/aws-eks-cluster-controller) |
| AWS EBS CSI Driver on Kubernetes | [kubernetes-sigs/aws-ebs-csi-driver](https://github.com/kubernetes-sigs/aws-ebs-csi-driver) |
| AWS EFS CSI Driver on Kubernetes | [kubernetes-sigs/aws-efs-csi-driver](https://github.com/kubernetes-sigs/aws-efs-csi-driver) |
| AWS EKS Charts | [aws/eks-charts](https://github.com/aws/eks-charts) |
| AWS Karpenter - Kubernetes Cluster Autoscaler | [aws/karpenter](https://github.com/aws/karpenter) |
| AWS Node Termination Handler - Gracefully handle EC2 instance shutdown within Kubernetes | [aws/aws-node-termination-handler](https://github.com/aws/aws-node-termination-handler) |
| Multus-CNI - enables attaching multiple network interfaces to pods in Kubernetes | [k8snetworkplumbingwg/multus-cni](https://github.com/k8snetworkplumbingwg/multus-cni) |

---
## Quick Start

- EKS Kubernetes [versions](https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions.html#kubernetes-release-calendar) and [release calendar](https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions.html#kubernetes-release-calendar)
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
- kube-bench is a tool that checks whether Kubernetes is deployed securely by running the checks documented in the CIS Kubernetes Benchmark. https://github.com/aquasecurity/kube-bench
- EKS Best Practices https://aws.github.io/aws-eks-best-practices/
- EKS Workshop https://www.eksworkshop.com
- AWSQS::Kubernetes::Helm https://github.com/aws-quickstart/quickstart-helm-resource-provider

---
## CDK for Kubernetes cdk8s
- [cdk8s-team/cdk8s](https://github.com/cdk8s-team/cdk8s)
- [cdk8s-team/cdk8s-cli](https://github.com/cdk8s-team/cdk8s-cli)
- [cdk8s-team/cdk8s-plus](https://github.com/cdk8s-team/cdk8s-plus)
- [aws-samples/amazon-eks-cdk-blue-green-cicd](https://github.com/aws-samples/amazon-eks-cdk-blue-green-cicd)

---
## EKS IAM OIDC Provider

This change is for restricting OpenIDConnectProvider created for EKS cluster from infra deploy roles and developer roles.

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

---
## EKS Persistent Storage
- https://aws.amazon.com/premiumsupport/knowledge-center/eks-persistent-storage/
- https://github.com/kubernetes-sigs/aws-ebs-csi-driver
- https://github.com/kubernetes-sigs/aws-efs-csi-driver

---
## EKS Logging
- https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Container-Insights-EKS-logs.html
- https://docs.aws.amazon.com/eks/latest/userguide/control-plane-logs.html
- https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/deploy-container-insights-EKS.html


---
## Collecting metrics with built-in Kubernetes monitoring tools
- https://www.datadoghq.com/blog/how-to-collect-and-graph-kubernetes-metrics/
    - Querying and visualizing resource metrics from Kubernetes
    - Gathering cluster-level status information
    - Viewing logs from Kubernetes pods

---
## Kubernetes Metrics Server
- https://docs.aws.amazon.com/eks/latest/userguide/metrics-server.html
- https://github.com/kubernetes/dashboard/blob/master/docs/user/integrations.md
- https://www.replex.io/blog/the-ultimate-guide-to-the-kubernetes-dashboard-how-to-install-and-integrate-metrics-server

```
# Deploy the Metrics Server

kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# Verify that the metrics-server deployment is running the desired number of pods with the following command

kubectl get deployment metrics-server -n kube-system
# NAME             READY   UP-TO-DATE   AVAILABLE   AGE
# metrics-server   1/1     1            1           57s

# Usage

# 1. View metric snapshots using kubectl top
kubectl top node
kubectl top pod --all-namespaces

# 2. Use kubectl get to query the Metrics API

# 2.a) To query the CPU and memory usage of a node
kubectl get --raw /apis/metrics.k8s.io/v1beta1/nodes/<NODE_NAME> | jq

# 2.b) To query the CPU and memory usage of a pod
kubectl get --raw /apis/metrics.k8s.io/v1beta1/namespaces/<NAMESPACE>/pods/<POD_NAME> | jq
```

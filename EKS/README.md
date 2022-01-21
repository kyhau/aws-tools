# EKS Notes

- Non-AWS Kubernetes tools: [kyhau/workspace/useful-tools/kubernetes](https://github.com/kyhau/workspace/tree/master/useful-tools/kubernetes)
- [QuickStart](#quick-start)
- [CDK for Kubernetes cdk8s](#cdk-for-Kubernetes-cdk8s)
- [EKS logging](#eks-logging)
- [Collecting metrics with built-in Kubernetes monitoring tools](#collecting-metrics-with-built-in-kubernetes-monitoring-tools)
- [Kubernetes Metrics Server](#kubernetes-metrics-server)

---
## Quick Start
- EKS Best Practices https://aws.github.io/aws-eks-best-practices/
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
- Amazon EKS Workshop https://www.eksworkshop.com

---
## CDK for Kubernetes cdk8s
- [cdk8s-team/cdk8s](https://github.com/cdk8s-team/cdk8s)
- [cdk8s-team/cdk8s-cli](https://github.com/cdk8s-team/cdk8s-cli)
- [cdk8s-team/cdk8s-plus](https://github.com/cdk8s-team/cdk8s-plus)

---
## EKS Persistent Storage
- https://aws.amazon.com/premiumsupport/knowledge-center/eks-persistent-storage/
- https://github.com/kubernetes-sigs/aws-ebs-csi-driver

---
## EKS logging
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

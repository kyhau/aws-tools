# MLTA (Monitoring / Logging / Tracing / Alerting)

Jump to
- [How does Amazon Managed Service for Prometheus relate to Amazon CloudWatch? Which one should I use?](#how-does-amazon-managed-service-for-prometheus-relate-to-amazon-cloudwatch-which-one-should-i-use)
- [CloudWatch metrics + AWS Distro for OpenTelemetry (ADOT) + Amazon Managed Service for Prometheus + Amazon Managed Grafana](#cloudwatch-metrics--aws-distro-for-opentelemetry-adot--amazon-managed-service-for-prometheus--amazon-managed-grafana)


---
## How does Amazon Managed Service for Prometheus relate to Amazon CloudWatch? Which one should I use?

**CloudWatch**

- Amazon CloudWatch is an AWS service that provides end-to-end observability across logs, metrics, and traces for applications running on EC2, AWS container services (EKS, ECS), Lambda, and other AWS services.
- Amazon CloudWatch can **discover and collect Prometheus metrics**, as CloudWatch metrics to provide options for our customers to query and alarm on Prometheus metrics.
- You should use Amazon CloudWatch if you are looking for a comprehensive observability service that brings together logs, metrics, tracing, dashboarding, and alerting in a unified experience that encompasses AWS services, EC2, containers, and serverless.

**Amazon Managed Service for Prometheus**

- Amazon Managed Service for Prometheus is specifically optimized for monitoring container-based workloads. Amazon Managed Service for Prometheus offers a Prometheus-compatible APIs for ingesting and querying your Prometheus metrics.
- Amazon Managed Service for Prometheus **is a metric-only service and does not collect logs or distributed trace data**. You can export selected CloudWatch metrics to Amazon Managed Service for Prometheus in order to use **PromQL** as the common query language for querying and alarming on all your stored metrics.
- You should use Amazon Managed Service for Prometheus if you want a service that is fully compatible with the Prometheus open source project. You should also choose Amazon Managed Service for Prometheus if you are already running Prometheus and are looking to eliminate that ongoing operational cost while also improving security.

See https://aws.amazon.com/prometheus/faqs/.


---
## CloudWatch metrics + AWS Distro for OpenTelemetry (ADOT) + Amazon Managed Service for Prometheus + Amazon Managed Grafana

- [Viewing Amazon CloudWatch metrics with Amazon Managed Service for Prometheus and Amazon Managed Grafana](https://aws.amazon.com/blogs/mt/viewing-amazon-cloudwatch-metrics-with-amazon-managed-service-for-prometheus-and-amazon-managed-grafana/)

# AWS Distro for OpenTelemetry (ADOT)

OpenTelemetry provides open-source APIs, libraries, and agents to collect distributed traces and metrics for application monitoring. With AWS Distro for OpenTelemetry, you can collect metadata from your AWS resources and managed services to correlate application performance data with underlying infrastructure data, reducing the mean time to problem resolution.

Jump to
- [Useful toolls](#useful-tools)
- Use Cases
    - [ADOT, CloudWatch, Amazon Managed Service for Prometheus, Amazon Managed Grafana](#adot-cloudwatch-amazon-managed-service-for-prometheus-amazon-managed-grafana)
    - [EKS with ADOT, X-Ray, CloudWatch, Amazon Managed Service for Prometheus](#eks-with-adot-x-ray-cloudwatch-amazon-managed-service-for-prometheus)
    - [Lambda functions](#lambda-functions)
- [How does Amazon Managed Service for Prometheus relate to Amazon CloudWatch? Which one should I use?](#how-does-amazon-managed-service-for-prometheus-relate-to-amazon-cloudwatch-which-one-should-i-use)


---
## Useful Tools

- [aws-otel-collector](https://github.com/aws-observability/aws-otel-collector) - AWS Distro for OpenTelemetry Collector (ADOT Collector) is an AWS supported version of the upstream OpenTelemetry Collector and is distributed by Amazon. It supports the selected components from the OpenTelemetry community. It is fully compatible with AWS computing platforms including EC2, ECS, EKS, and Docker. It enables users to send telemetry data to AWS CloudWatch Metrics, Traces, and Logs backends as well as the other supported backends.

- [aws-otel-helm-charts](https://github.com/aws-observability/aws-otel-helm-charts) - AWS Distro for OpenTelemetry (ADOT) Helm Charts

- [aws-otel-lambda](https://github.com/aws-observability/aws-otel-lambda) - AWS managed OpenTelemetry Lambda Layers

- SDKs or libraries
    - [aws-otel-dotnet](https://github.com/aws-observability/aws-otel-dotnet) - AWS Distro for OpenTelemetry .NET
    - [aws-otel-go](https://github.com/aws-observability/aws-otel-go) - AWS Distro for OpenTelemetry Go
    - [aws-otel-js](https://github.com/aws-observability/aws-otel-js) - AWS Distro for OpenTelemetry JavaScript
    - [aws-otel-python](https://github.com/aws-observability/aws-otel-python) - AWS Distro for OpenTelemetry Python
    - [aws-otel-ruby](https://github.com/aws-observability/aws-otel-ruby) - AWS Distro for OpenTelemetry Ruby
    - [aws-otel-java-instrumentation](https://github.com/aws-observability/aws-otel-java-instrumentation) - AWS Distro for OpenTelemetry - Instrumentation for Java

- [Lambda Telemetry API](https://docs.aws.amazon.com/lambda/latest/dg/telemetry-api.html)


---
## Use Cases

### ADOT, CloudWatch, Amazon Managed Service for Prometheus, Amazon Managed Grafana

- [Viewing Amazon CloudWatch metrics with Amazon Managed Service for Prometheus and Amazon Managed Grafana](https://aws.amazon.com/blogs/mt/viewing-amazon-cloudwatch-metrics-with-amazon-managed-service-for-prometheus-and-amazon-managed-grafana/)

### EKS with ADOT, X-Ray, CloudWatch, Amazon Managed Service for Prometheus

- [Adding metrics and traces to your application on Amazon EKS with AWS Distro for OpenTelemetry, AWS X-Ray and Amazon CloudWatch](https://aws.amazon.com/blogs/mt/adding-metrics-and-traces-to-your-application-on-amazon-eks-with-aws-distro-for-opentelemetry-aws-x-ray-and-amazon-cloudwatch/)

### Lambda functions

- Using the [Lambda Telemetry API](https://docs.aws.amazon.com/lambda/latest/dg/telemetry-api.html), your Lambda extensions can directly receive telemetry data from Lambda. During function initialization and invocation, Lambda automatically captures telemetry, such as logs, platform metrics, and platform traces. With Telemetry API, extensions can get this telemetry data directly from Lambda in near real time.
    - AWS Partner Network (APN) partners: Coralogix, Datadog, Dynatrace, Lumigo, New Relic, Sedai, Serverless.com, Site24x7, Sumo Logic, Sysdig, and Thundra.
- [aws-otel-lambda](https://github.com/aws-observability/aws-otel-lambda) - AWS managed OpenTelemetry Lambda Layers


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

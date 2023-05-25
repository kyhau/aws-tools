
# Security

- [Useful Libs and Tools](#useful-libs-and-tools)
- [Useful Articles and Blogs](#useful-articles-and-blogs)
- [Incident Response](#incident-response)
- [Configure mutual Transport Layer Security (mutual TLS or mTLS) authentication with AWS services](#configure-mutual-transport-layer-security-mutual-tls-or-mtls-authentication-with-aws-services)
- [Options for granular control on TLS cipher suites](#options-for-granular-control-on-tls-cipher-suites)
- [Firewall Manager, WAF, Shield](./WAF-FirewallManager-Shield/README.md)
- [IAM](./IAM/)
- [Instance Metadata Service (IMDS)](./Security/aws_metadata/)
- [GuardDuty](./GuardDuty/)
- [Security Hub](./SecurityHub/)

---
## Useful Libs and Tools

- Amazon Security Bulletins - https://aws.amazon.com/security/security-bulletins/
- Amazon Linux Security Center - https://alas.aws.amazon.com/announcements.html
- Amazon Detective Multiaccount Scripts - [aws-samples/amazon-detective-multiaccount-scripts](https://github.com/aws-samples/amazon-detective-multiaccount-scripts)
- Amazon Security Lake Resources [aws-samples/amazon-security-lake](https://github.com/aws-samples/amazon-security-lake)
- AWS Security Benchmark - [awslabs/aws-security-benchmark](https://github.com/awslabs/aws-security-benchmark)
- AWS Self-Service Security Assessment tool - [awslabs/aws-security-assessment-solution](https://github.com/awslabs/aws-security-assessment-solution)
- Open source tools for AWS security - [toniblyx/my-arsenal-of-aws-security-tools](https://github.com/toniblyx/my-arsenal-of-aws-security-tools)
- Ultimate DevSecOps library - [sottlmarek/DevSecOps](https://github.com/sottlmarek/DevSecOps)
- cloud-custodian - [cloud-custodian/cloud-custodian](https://github.com/cloud-custodian/cloud-custodian)
- CloudGoat - [RhinoSecurityLabs/cloudgoat](https://github.com/RhinoSecurityLabs/cloudgoat)
- git-secrets - [awslabs/git-secrets](https://github.com/awslabs/git-secrets)
- Pacu an open source AWS exploitation framework - [RhinoSecurityLabs/Pacu](https://github.com/RhinoSecurityLabs/pacu)
- Redboto - [elitest/Redboto](https://github.com/elitest/Redboto)
- Endgame: Creating Backdoors in AWS - [hirajanwin/endgame](https://github.com/hirajanwin/endgame)
- Endgame: AWS Pentesting tool - [DavidDikker/endgame](https://github.com/DavidDikker/endgame)


---
## Useful Articles and Blogs

- SSM Parameter Store SecureString vs. Secrets Manager - [Handling Secrets with AWS](https://www.lastweekinaws.com/blog/handling-secrets-with-aws/), 2022
- AWS Exposable Resources - [SummitRoute/aws_exposable_resources](https://github.com/SummitRoute/aws_exposable_resources) - this repo maintains a list of all AWS resources that can be publicly exposed.
- AWS Security Documentation by Category - [docs.aws.amazon.com/security](https://docs.aws.amazon.com/security/)
- AWS Security Reference Architecture (AWS SRA) - [docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/](https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/architecture.html)
- A Secure Cloud - Repository of customizable AWS security configurations and best practices - [asecure.cloud/](https://asecure.cloud/)


---
## Incident Response

- [aws-samples/automated-incident-response-with-ssm](https://github.com/aws-samples/automated-incident-response-with-ssm) - Automated Incident Response with SSM
- [easttimor/aws-incident-response](https://github.com/easttimor/aws-incident-response) - Investigation of API activity using Athena and notification of actions using EventBridge


---
## Configure mutual Transport Layer Security (mutual TLS or mTLS) authentication with AWS services

### General

- In order to support doing TLS handshake for mTLS, you need a L4 load balancer like AWS NLB, not ALB.
- Public AWS ACM does not allow you to export private key which means your client won’t be able to present the client certificate to validate. You might need to use things like [Private Certificate Authority - AWS Certificate Manager - Amazon Web Services (AWS) 7](https://aws.amazon.com/certificate-manager/private-certificate-authority/) or some other CA to generate client certificate for you. See [this Stack Overflow post - How do I get client certificate from ACM?](https://stackoverflow.com/questions/64606582/how-do-i-get-client-certificate-from-acm).

### How to configure mTLS authentication for applications running on Amazon EKS

- NLB → NGINX → Application service and pod
- [Configure mutual TLS authentication for applications running on Amazon EKS](https://docs.aws.amazon.com/prescriptive-guidance/latest/patterns/configure-mutual-tls-authentication-for-applications-running-on-amazon-eks.html)

### How to configure mTLS authentication for Amazon API Gateway

- [Configuring mutual TLS authentication for a REST API](https://docs.aws.amazon.com/apigateway/latest/developerguide/rest-api-mutual-tls.html)
- [Automating mutual TLS setup for Amazon API Gateway](https://aws.amazon.com/blogs/compute/automating-mutual-tls-setup-for-amazon-api-gateway/)
- [Introducing mutual TLS authentication for Amazon API Gateway](https://aws.amazon.com/blogs/compute/introducing-mutual-tls-authentication-for-amazon-api-gateway/)
- [Propagating valid mTLS client certificate identity to downstream services using Amazon API Gateway](https://aws.amazon.com/blogs/compute/propagating-valid-mtls-client-certificate-identity-to-downstream-services-using-amazon-api-gateway/)
    - Repo: https://github.com/aws-samples/api-gateway-certificate-propagation

### How to configure mTLS authentication for AWS App Mesh

- [How to use ACM Private CA for enabling mTLS in AWS App Mesh](https://aws.amazon.com/blogs/security/how-to-use-acm-private-ca-for-enabling-mtls-in-aws-app-mesh/)
- [Three things to consider when implementing Mutual TLS with AWS App Mesh](https://aws.amazon.com/blogs/containers/three-things-to-consider-when-implementing-mutual-tls-with-aws-app-mesh/)
- https://docs.aws.amazon.com/app-mesh/latest/userguide/mutual-tls.html


---
## Options for granular control on TLS cipher suites

If you want to exclude specific ciphers, you can use the following solutions to offload and control the TLS connection termination with a customized cipher suite:
1. Network Load Balancer
2. CloudFront distribution
3. Self-managed reverse proxy

See [Exclude cipher suites at the API gateway using a Network Load Balancer security policy](https://aws.amazon.com/blogs/security/exclude-cipher-suites-at-the-api-gateway-using-a-network-load-balancer-security-policy/)
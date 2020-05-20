# arki

Some tools and sample code I created for building with AWS.

[![githubactions](https://github.com/kyhau/arki/workflows/Build-Test/badge.svg)](https://github.com/kyhau/arki/actions)
[![travisci](https://travis-ci.org/kyhau/arki.svg?branch=master)](https://travis-ci.org/kyhau/arki)
[![codecov](https://codecov.io/gh/kyhau/arki/branch/master/graph/badge.svg)](https://codecov.io/gh/kyhau/arki)

```
# Create virtual env and install the required packages

virtualenv env -p python3.8
. env/bin/activate
pip install -r requirements.txt
```

# Categories
- [AWS SDKs and CLIs](#aws-sdks-and-clis)
  - [CloudFormation](#cloudformation)
  - [Serverless](#serverless)
  - [Security](#security)
- [Some useful tools required deployment](#some-useful-tools-required-deployment)
  - [Networking](#networking)
- [Other tools](#other-tools)
- [Best Practices Guides](#best-practices-guides)
- [Workshops](#workshops)
- [kyhau/aws-notebook](https://github.com/kyhau/aws-notebook)

---
## AWS SDKs and CLIs

| Description | Repo/Link |
| :--- | :--- |
| Amazon CloudWatch Embedded Metric Format Client Library | [awslabs/aws-embedded-metrics-python](https://github.com/awslabs/aws-embedded-metrics-python) |
| Amazon ECR Docker Credential Helper | [awslabs/amazon-ecr-credential-helper](https://github.com/awslabs/amazon-ecr-credential-helper) |
| Amazon ECS CLI v2 | [aws/amazon-ecs-cli-v2](https://aws.amazon.com/blogs/containers/announcing-the-amazon-ecs-cli-v2/) |
| Amazon EKS CLI | [weaveworks/eksctl](https://github.com/weaveworks/eksctl) |
| Amazon EKS-vended aws-iam-authenticator | [Amazon EKS-vended aws-iam-authenticator](https://docs.aws.amazon.com/eks/latest/userguide/install-aws-iam-authenticator.html) |
| Amazon EKS-vended kubectl | [Amazon EKS-vended kubectl](https://docs.aws.amazon.com/eks/latest/userguide/install-kubectl.html) |
| Authorization Lambda@Edge (nodejs) | [aws-samples/authorization-lambda-at-edge](https://github.com/aws-samples/authorization-lambda-at-edge) |
| AWS CLI | [aws/aws-cli](https://github.com/aws/aws-cli) |
| AWS CLI interactive productivity booster (aws-shell) | [awslabs/aws-shell](https://github.com/awslabs/aws-shell) |
| AWS Config Rules Development Kit (RDK) | [awslabs/aws-config-rdk](https://github.com/awslabs/aws-config-rdk) |
| AWS Config Rules RDK Python library | [awslabs/aws-config-rdklib](https://github.com/awslabs/aws-config-rdklib) |
| AWS DynamoDB Encryption Client for Python | [aws/aws-dynamodb-encryption-python](https://github.com/aws/aws-dynamodb-encryption-python) |
| AWS EC2 ENI Utilities (ec2-net-utils)  | [aws/ec2-net-utils](https://github.com/aws/ec2-net-utils) |
| AWS EFS Utilities (efs-utils)  | [aws/efs-utils](https://github.com/aws/efs-utils) |
| AWS Elastic Beanstalk CLI | [aws/aws-elastic-beanstalk-cli](https://github.com/aws/aws-elastic-beanstalk-cli) |
| AWS Encryption SDK (Python) | [aws/aws-encryption-sdk-python](https://github.com/aws/aws-encryption-sdk-python) |
| AWS Encryption SDK CLI | [aws/aws-encryption-sdk-cli](https://github.com/aws/aws-encryption-sdk-cli) |
| AWS IoT Greengrass Core SDK (Python) | [aws/aws-greengrass-core-sdk-python](https://github.com/aws/aws-greengrass-core-sdk-python) |
| AWS IoT Device SDK (Python) | [aws/aws-iot-device-sdk-python](https://github.com/aws/aws-iot-device-sdk-python) |
| AWS ParallelCluster (enhanced version of CfnCluster) | [aws/aws-parallelcluster](https://github.com/aws/aws-parallelcluster) |
| AWS SageMaker SDK (Python) | [aws/sagemaker-python-sdk](https://github.com/aws/sagemaker-python-sdk) |
| AWS Tools for Microsoft VSTS | [AWS Tools for Microsoft Visual Studio Team Services](https://docs.aws.amazon.com/vsts/latest/userguide/welcome.html) |
| AWS Tools for PowerShell | [AWS Tools for PowerShell](https://aws.amazon.com/powershell/) |
| AWS Tools and sample code provided by AWS Premium Support | [awslabs/aws-support-tools](https://github.com/awslabs/aws-support-tools) |
| AWS Trusted Advisor Tools | [aws/Trusted-Advisor-Tools](https://github.com/aws/Trusted-Advisor-Tools) |
| AWS X-Ray SDK (Python) | [aws/aws-xray-sdk-python](https://github.com/aws/aws-xray-sdk-python) |
| bash-my-aws | [bash-my-universe/bash-my-aws](https://github.com/bash-my-universe/bash-my-aws.git) |
| kubectl | [kubernetes/kubectl](https://github.com/kubernetes/kubectl) |
| Warrant a Python library for using AWS Cognito with support for SRP| [capless/warrant](https://github.com/capless/warrant) |

### CDK
| Description | Repo/Link |
| :--- | :--- |
| AWS Cloud Development Kit (CDK) | [aws/aws-cdk](https://github.com/aws/aws-cdk) |
| [CDK for Kubernetes (cdk8s)](https://cdk8s.io/) | [awslabs/cdk8s](https://github.com/awslabs/cdk8s) |

### CloudFormation

| Description | Repo/Link |
| :--- | :--- |
| AWS CloudFormation CLI (cloudformation-cli) | [aws-cloudformation/aws-cloudformation-cli](https://github.com/aws-cloudformation/cloudformation-cli) |
| AWS CloudFormation Linter (cfn-lint)  | [aws-cloudformation/cfn-python-lint](https://github.com/aws-cloudformation/cfn-python-lint) |
| AWS CloudFormation Resources and Projects | [aws-cloudformation/awesome-cloudformation](https://github.com/aws-cloudformation/awesome-cloudformation) |
| AWS CloudFormation Resource Provider Python Plugin | [aws-cloudformation/cloudformation-cli-python-plugin](https://github.com/aws-cloudformation/cloudformation-cli-python-plugin) |
| AWS CloudFormation Sample Templates | [awslabs/aws-cloudformation-templates](https://github.com/awslabs/aws-cloudformation-templates) |
| AWS CloudFormation Template Flip (cfn-flip) | [awslabs/aws-cfn-template-flip](https://github.com/awslabs/aws-cfn-template-flip) |
| CloudMapper | [duo-labs/cloudmapper](https://github.com/duo-labs/cloudmapper) |
| CloudFormer | [CloudFormer for creating templates from existing AWS resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-using-cloudformer.html) |
| Former2 generates CloudFormation / Terraform / Troposphere templates from existing AWS resources | [iann0036/former2](https://github.com/iann0036/former2) |

### Serverless

| Description | Repo/Link |
| :--- | :--- |
| AWS Chalice - Python Serverless Microframework for AWS | [aws/chalice](https://github.com/aws/chalice) |
| AWS Serverless Application Model (SAM) | [awslabs/serverless-application-model](https://github.com/awslabs/serverless-application-model) |
| AWS Serverless Application Model (SAM) CLI | [awslabs/aws-sam-cli](https://github.com/awslabs/aws-sam-cli) 
| AWS Serverless Application Repository | [AWS Serverless Application Repository](https://aws.amazon.com/serverless/serverlessrepo/) |
| AWS Step Functions Data Science SDK (Python) | [aws/aws-step-functions-data-science-sdk-python](https://github.com/aws/aws-step-functions-data-science-sdk-python) |
| LocalStack | [localstack](https://github.com/localstack/localstack) |
| LocalStack AWS CLI (awslocal) | [awscli-local](https://github.com/localstack/awscli-local) |
| Serverless Framework | [serverless/serverless](https://github.com/serverless/serverless) |
| Serverless Components | [serverless/components](https://github.com/serverless/components) |
| Serverless Components CLI | [serverless/cli](https://github.com/serverless/cli) |
| Stelligent mu (a tool for managing your microservices platform) | [stelligent/mu](https://github.com/stelligent/mu) |
| Zappa Serverless Python | [Miserlou/Zappa](https://github.com/Miserlou/Zappa) |

### Security

| Description | Repo/Link |
| :--- | :--- |
| AWS Security Documentation by Category | [docs.aws.amazon.com/security](https://docs.aws.amazon.com/security/)|
| A Secure Cloud - Repository of customizable AWS security configurations and best practices | [asecure.cloud/](https://asecure.cloud/) |
| Open source tools for AWS security | [toniblyx/my-arsenal-of-aws-security-tools](https://github.com/toniblyx/my-arsenal-of-aws-security-tools) |
| AWS IAM Policy Simulator | [IAM Policy Simulator Console](https://policysim.aws.amazon.com/) |
| AWS Policy Generator | [AWS Policy Generator](https://awspolicygen.s3.amazonaws.com/policygen.html) |
| AWS Security Benchmark | [awslabs/aws-security-benchmark](https://github.com/awslabs/aws-security-benchmark) |
| AWS Security Hub Multiaccount Scripts | [awslabs/aws-securityhub-multiaccount-scripts](https://github.com/awslabs/aws-securityhub-multiaccount-scripts) |
| Import AWS Config Findings into AWS Security Hub | [aws-samples/aws-securityhub-config-integration](https://github.com/aws-samples/aws-securityhub-config-integration) |
| aws-securityhub-to-email | [aws-samples/aws-securityhub-to-email](https://github.com/aws-samples/aws-securityhub-to-email) |
| aws-securityhub-to-slack | [aws-samples/aws-securityhub-to-slack](https://github.com/aws-samples/aws-securityhub-to-slack) |
| cloud-custodian | [cloud-custodian/cloud-custodian](https://github.com/cloud-custodian/cloud-custodian) |
| CloudGoat | [RhinoSecurityLabs/cloudgoat](https://github.com/RhinoSecurityLabs/cloudgoat) |
| git-secrets | [awslabs/git-secrets](https://github.com/awslabs/git-secrets) |
| Pacu an open source AWS exploitation framework | [RhinoSecurityLabs/Pacu](https://github.com/RhinoSecurityLabs/pacu) |

## Some useful tools

| Description | Repo/Link |
| :--- | :--- |
| Amazon DynamoDB NoSQL Workbench | [NoSQL Workbench for Amazon DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/workbench.html) |
| AWS Auto Scaling Custom Resources | [aws/aws-auto-scaling-custom-resource](https://github.com/aws/aws-auto-scaling-custom-resource) |
| AWS Deployment Framework (ADF) | [awslabs/aws-deployment-framework](https://github.com/awslabs/aws-deployment-framework) |
| AWS Distributed Load Testing | [awslabs/distributed-load-testing-on-aws](https://github.com/awslabs/distributed-load-testing-on-aws) |
| AWS Instance Scheduler | [AWS Instance Scheduler](https://aws.amazon.com/solutions/instance-scheduler/) |
| AWS Multi Account Viewer | [awslabs/aws-multi-account-viewer](https://github.com/awslabs/aws-multi-account-viewer) |
| awslimitchecker | [jantman/awslimitchecker](https://github.com/jantman/awslimitchecker) |

### Networking

| Description | Repo/Link |
| :--- | :--- |
| AWS CIDR Finder | [aws-samples/aws-cidr-finder](https://github.com/aws-samples/aws-cidr-finder) | 
| [Serverless Transit Network Orchestrator](https://aws.amazon.com/solutions/serverless-transit-network-orchestrator/) | [awslabs/serverless-transit-network-orchestrator](https://github.com/awslabs/serverless-transit-network-orchestrator) |
| TGW (Transit Gateway) Migrator Tool | [TGW Migrator Tool](https://aws.amazon.com/blogs/networking-and-content-delivery/migrate-from-transit-vpc-to-aws-transit-gateway/) |
| TGW to solve overlapping CIDRs | [aws-samples/aws-transit-gateway-overlapping-cidrs](https://github.com/aws-samples/aws-transit-gateway-overlapping-cidrs) |

## Other tools

| Description | Repo/Link |
| :--- | :--- |
| FastAPI | [tiangolo/fastapi](https://github.com/tiangolo/fastapi) |
| Regex tester and debugger: PHP, PCRE, Python, Golang and JavaScript | [regex101.com](https://regex101.com/) |
| Subnet Calculator - MxToolbox | [mxtoolbox.com](https://mxtoolbox.com/subnetcalculator.aspx) |

## Best Practices Guides
- [Amazon EKS Best Practices Guide for Security](https://aws.github.io/aws-eks-best-practices/), AWS

## Workshops
- [Asynchronous Messaging](https://github.com/aws-samples/asynchronous-messaging-workshop)
- [CDK](https://cdkworkshop.com/)
- [CI/CD for Serverless Applications](https://cicd.serverlessworkshops.io/)
- [Redshift Immersion](https://redshift-immersion.workshop.aws)

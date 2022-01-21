# aws-tools

Some tools and sample code I created for building with AWS.

Most of the Python scripts support multi accounts and regions.

[![githubactions](https://github.com/kyhau/aws-tools/workflows/Build-Test/badge.svg)](https://github.com/kyhau/aws-tools/actions)
[![travisci](https://travis-ci.org/kyhau/aws-tools.svg?branch=master)](https://travis-ci.org/kyhau/aws-tools)
[![codecov](https://codecov.io/gh/kyhau/aws-tools/branch/master/graph/badge.svg)](https://codecov.io/gh/kyhau/aws-tools)

## For running Python scripts

Python 3.6 +

```
# Create and activate virtual env (optional)
virtualenv env -p python3.10
. env/bin/activate

# Install the required packages
pip install -r requirements.txt

# Optional
source .aliases
```

## For running shell scripts

```
pip install -r requirements-cli.txt
```

---
## Useful Links
- [CDK v1 and v2](#cdk)
- [CloudFormation](#cloudformation)
- [Serverless](#serverless)
- [ECS, EKS, container-based development](#ecs-eks-container-based-development)
- [AWS SDKs and CLIs](#aws-sdks-and-clis)
- [Security](#security)
- [Chaos Engineering](#chaos-engineering)
- [Networking](#networking)
- [Visualisation](https://github.com/kyhau/aws-resource-visualisation/)
- [Closing account](#closing-account)
- [Other AWS useful tools](#other-aws-useful-tools)
- [Data sources](#data-sources)
- [Other tools](#other-tools)
- [Best Practices Guides](#best-practices-guides)
- [Workshops](#workshops)
- [kyhau/aws-notebook](https://github.com/kyhau/aws-notebook)

---

### CDK

| Description | Repo/Link |
| :--- | :--- |
| AWS CDK (Cloud Development Kit) | [aws/aws-cdk](https://github.com/aws/aws-cdk) |
| AWS CDK Construct Hub - Find reusable components for your cloud applications | [constructs.dev](https://constructs.dev/) |
| [AWS CDK for Kubernetes (cdk8s)](https://cdk8s.io/) | [cdk8s-team/cdk8s](https://github.com/cdk8s-team/cdk8s) |
| AWS cdk8s-cli - a command-line-interface for CDK for Kubernetes | [cdk8s-team/cdk8s-cli](https://github.com/cdk8s-team/cdk8s-cli) |
| [AWS CDK Assume Role Credential Plugin](https://aws.amazon.com/blogs/devops/cdk-credential-plugin/) | [aws-samples/cdk-assume-role-credential-plugin](https://github.com/aws-samples/cdk-assume-role-credential-plugin) |
| [AWS Solutions Constructs](https://docs.aws.amazon.com/solutions/latest/constructs/api-reference.html) | [awslabs/aws-solutions-constructs](https://github.com/awslabs/aws-solutions-constructs) |
| CDK Patterns | [cdk-patterns/serverless](https://github.com/cdk-patterns/serverless) |
| Serverless Stack Toolkit (SST) (extension of AWS CDK) | [serverless-stack/serverless-stack](https://github.com/serverless-stack/serverless-stack) |
| Awesome CDK | [kolomied/awesome-cdk](https://github.com/kolomied/awesome-cdk) |
| kyhau/cdk-examples (CDK v1 and v2) | [kyhau/cdk-examples](https://github.com/kyhau/cdk-examples) |

### CloudFormation

| Description | Repo/Link |
| :--- | :--- |
| AWS CloudFormation CLI (cfn) | [aws-cloudformation/aws-cloudformation-cli](https://github.com/aws-cloudformation/cloudformation-cli) |
| AWS CloudFormation Guard (cfn-guard) | [aws-cloudformation/cloudformation-guard](https://github.com/aws-cloudformation/cloudformation-guard) |
| AWS CloudFormation Handling Region parity| [aws-samples/aws-cloudformation-region-parity](https://github.com/aws-samples/aws-cloudformation-region-parity) |
| AWS CloudFormation Linter (cfn-lint) | [aws-cloudformation/cfn-python-lint](https://github.com/aws-cloudformation/cfn-python-lint) |
| AWS CloudFormation Macros | [aws-cloudformation/aws-cloudformation-macros](https://github.com/aws-cloudformation/aws-cloudformation-macros) |
| AWS CloudFormation Registry (public/private extensions/modules) | [User Guide](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) |
| AWS CloudFormation Resource Provider Python Plugin | [aws-cloudformation/cloudformation-cli-python-plugin](https://github.com/aws-cloudformation/cloudformation-cli-python-plugin) |
| AWS CloudFormation Resources and Projects | [aws-cloudformation/awesome-cloudformation](https://github.com/aws-cloudformation/awesome-cloudformation) |
| AWS CloudFormation Sample Templates | [awslabs/aws-cloudformation-templates](https://github.com/awslabs/aws-cloudformation-templates) |
| AWS CloudFormation Template Flip (cfn-flip) | [awslabs/aws-cfn-template-flip](https://github.com/awslabs/aws-cfn-template-flip) |
| [AWS predefined CloudWatch metric filters and alarms](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/use-cloudformation-template-to-create-cloudwatch-alarms.html) |[CloudWatch_Alarms_for_CloudTrail_API_Activity.zip](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/samples/CloudWatch_Alarms_for_CloudTrail_API_Activity.zip)|
| AWSUtility::CloudFormation::CommandRunner | [aws-cloudformation/aws-cloudformation-resource-providers-awsutilities-commandrunner](https://github.com/aws-cloudformation/aws-cloudformation-resource-providers-awsutilities-commandrunner) |
| CloudMapper | [duo-labs/cloudmapper](https://github.com/duo-labs/cloudmapper) |
| CloudFormer | [CloudFormer for creating templates from existing AWS resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-using-cloudformer.html) |
| Former2 generates CloudFormation / Terraform / Troposphere templates from existing AWS resources | [iann0036/former2](https://github.com/iann0036/former2) |

### Serverless

| Description | Repo/Link |
| :--- | :--- |
| Amazon API Gateway CORS Configurator | [aws-samples/amazon-api-gateway-cors-configurator](https://github.com/aws-samples/amazon-api-gateway-cors-configurator) |
| [Amazon API Gateway Serverless Developer Portal](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-developer-portal.html) | [awslabs/aws-api-gateway-developer-portal](https://github.com/awslabs/aws-api-gateway-developer-portal) |
| AWS Chalice - Python Serverless Microframework for AWS | [aws/chalice](https://github.com/aws/chalice) |
| AWS Lambda Builders (Python library, the brains behind `sam build`) | [aws/aws-lambda-builders](https://github.com/aws/aws-lambda-builders) |
| AWS Lambda Developer Guide | [awsdocs/aws-lambda-developer-guide](https://github.com/awsdocs/aws-lambda-developer-guide) |
| AWS Lambda Extensions API | [specification](https://docs.aws.amazon.com/lambda/latest/dg/runtimes-extensions-api.html) |
| AWS Lambda Extensions sample projects | [aws-samples/aws-lambda-extensions](https://github.com/aws-samples/aws-lambda-extensions/) |
| AWS Lambda Logs API | [specification](https://docs.aws.amazon.com/lambda/latest/dg/runtimes-logs-api.html) |
| AWS Lambda Powertools | [awslabs/aws-lambda-powertools-python](https://github.com/awslabs/aws-lambda-powertools-python) |
| AWS Lambda Power Tuning | [alexcasalboni/aws-lambda-power-tuning](https://github.com/alexcasalboni/aws-lambda-power-tuning) |
| AWS Lambda Python Runtime Interface Client | [aws/aws-lambda-python-runtime-interface-client](https://github.com/aws/aws-lambda-python-runtime-interface-client) |
| AWS Lambda Runtime API | [specification](https://docs.aws.amazon.com/lambda/latest/dg/runtimes-api.html) |
| AWS Lambda Runtime Interface Emulator | [aws/aws-lambda-runtime-interface-emulator](https://github.com/aws/aws-lambda-runtime-interface-emulator/) |
| AWS Serverless Application Model (SAM) | [awslabs/serverless-application-model](https://github.com/awslabs/serverless-application-model) |
| AWS Serverless Application Model (SAM) CLI | [awslabs/aws-sam-cli](https://github.com/awslabs/aws-sam-cli)
| AWS Serverless Application Model (SAM) Examples | [awslabs/serverless-application-model/examples/](https://github.com/awslabs/serverless-application-model/tree/master/examples/2016-10-31) |
| Cookiecutter SAM for Python Lambda functions | [aws-samples/cookiecutter-aws-sam-python](https://github.com/aws-samples/cookiecutter-aws-sam-python) |
| AWS Serverless Patterns (SAM, CDK) | [aws-samples/serverless-patterns](https://github.com/aws-samples/serverless-patterns) |
| AWS Serverless Application Repository | [AWS Serverless Application Repository](https://aws.amazon.com/serverless/serverlessrepo/) |
| AWS Step Functions Data Science SDK (Python) | [aws/aws-step-functions-data-science-sdk-python](https://github.com/aws/aws-step-functions-data-science-sdk-python) |
| A sandboxed local environment that replicates the live AWS Lambda environment | [lambci/docker-lambda](https://github.com/lambci/docker-lambda) |
| LocalStack | [localstack/localstack](https://github.com/localstack/localstack) |
| LocalStack AWS CLI (awslocal) | [ocalstack/awscli-local](https://github.com/localstack/awscli-local) |
| Serverless Framework | [serverless/serverless](https://github.com/serverless/serverless) |
| Serverless Components | [serverless/components](https://github.com/serverless/components) |
| Serverless Components CLI | [serverless/cli](https://github.com/serverless/cli) |
| Serverless Patterns Collection (SAM, CDK) | [serverlessland.com/patterns](https://serverlessland.com/patterns) |
| Serverless Stack (SST) (extension of CDK) | [serverless-stack/serverless-stack](https://github.com/serverless-stack/serverless-stack) |
| Stelligent mu (a tool for managing your microservices platform) | [stelligent/mu](https://github.com/stelligent/mu) |
| Zappa Serverless Python | [Miserlou/Zappa](https://github.com/Miserlou/Zappa) |
| Serverless Microservice Patterns for AWS | [Blog post](https://www.jeremydaly.com/serverless-microservice-patterns-for-aws/)|

### ECS, EKS, Container-based development

| ECS / ECR / Others | Repo/Link |
| :--- | :--- |
| Amazon ECR Docker Credential Helper | [awslabs/amazon-ecr-credential-helper](https://github.com/awslabs/amazon-ecr-credential-helper) |
| Amazon ECR Public Gallery | https://gallery.ecr.aws/ |
| Amazon ECS CLI v2 | [aws/amazon-ecs-cli-v2](https://aws.amazon.com/blogs/containers/announcing-the-amazon-ecs-cli-v2/) |
| Amazon ECS Exec | [Using ECS Exec to access containers on Fargate and EC2](https://aws.amazon.com/blogs/containers/new-using-amazon-ecs-exec-access-your-containers-fargate-ec2/) |
| AWS Copilot CLI - containerize apps on ECS/Fargate| [aws/copilot-cli](https://github.com/aws/copilot-cli) |
| AWS Fargate Fast AutoScaler (with CDK) | [aws-samples/aws-fargate-fast-autoscaler](https://github.com/aws-samples/aws-fargate-fast-autoscaler) |
| Docker CLI plugin for ECS | [docker/ecs-plugin](https://github.com/docker/ecs-plugin) |
| AWS App2Container | [Containerize a Java or .NET app](https://docs.aws.amazon.com/app2container/latest/UserGuide/start-intro.html) |
| Lazydocker - A simple terminal UI for both docker and docker-compose | [jesseduffield/lazydocker](https://github.com/jesseduffield/lazydocker) |


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
| AWS EBS CSI Driver on Kubernetes | [kubernetes-sigs/aws-ebs-csi-driver](https://github.com/kubernetes-sigs/aws-ebs-csi-driver) |
| AWS EFS CSI Driver on Kubernetes | [kubernetes-sigs/aws-efs-csi-driver](https://github.com/kubernetes-sigs/aws-efs-csi-driver) |
| AWS EKS Charts | [aws/eks-charts](https://github.com/aws/eks-charts) |
| AWS Karpenter - Kubernetes Cluster Autoscaler | [aws/karpenter](https://github.com/aws/karpenter) |
| AWS Node Termination Handler - Gracefully handle EC2 instance shutdown within Kubernetes | [aws/aws-node-termination-handler](https://github.com/aws/aws-node-termination-handler) |
| Multus-CNI - enables attaching multiple network interfaces to pods in Kubernetes | [k8snetworkplumbingwg/multus-cni](https://github.com/k8snetworkplumbingwg/multus-cni) |


## AWS SDKs and CLIs

| Description | Repo/Link |
| :--- | :--- |
| Amazon CloudWatch Embedded Metric Format Client Library (Python) | [awslabs/aws-embedded-metrics-python](https://github.com/awslabs/aws-embedded-metrics-python) |
| Amazon Ion Python | [amzn/ion-python](https://github.com/amzn/ion-python) |
| Amazon Neptune Tools | [awslabs/amazon-neptune-tools](https://github.com/awslabs/amazon-neptune-tools) |
| Amazon Redshift connector (for Python) | [aws/amazon-redshift-python-driver](https://github.com/aws/amazon-redshift-python-driver) |
| Authorization Lambda@Edge (Node.js) | [aws-samples/authorization-lambda-at-edge](https://github.com/aws-samples/authorization-lambda-at-edge) |
| AutoML Toolkit for Deep Learning | [awslabs/autogluon](https://github.com/awslabs/autogluon) |
| AWS Amplify CLI | [aws-amplify/amplify-cli](https://github.com/aws-amplify/amplify-cli) |
| AWS Amplify Flutter | [aws-amplify/amplify-flutter](https://github.com/aws-amplify/amplify-flutter) |
| AWS Cloud Digital Interface (CDI) Software Development Kit (SDK) | [aws/aws-cdi-sdk](https://github.com/aws/aws-cdi-sdk) |
| AWS CLI | [aws/aws-cli](https://github.com/aws/aws-cli) |
| AWS CLI interactive productivity booster (aws-shell) | [awslabs/aws-shell](https://github.com/awslabs/aws-shell) |
| AWS Config Rules Development Kit (RDK) CLI | [awslabs/aws-config-rdk](https://github.com/awslabs/aws-config-rdk) |
| AWS Config Rules Development Kit (RDK) Library (Python) | [awslabs/aws-config-rdklib](https://github.com/awslabs/aws-config-rdklib) |
| AWS DynamoDB Encryption Client (Python) | [aws/aws-dynamodb-encryption-python](https://github.com/aws/aws-dynamodb-encryption-python) |
| AWS EC2 ENI Utilities (ec2-net-utils)  | [aws/ec2-net-utils](https://github.com/aws/ec2-net-utils) |
| AWS EFS Utilities (efs-utils)  | [aws/efs-utils](https://github.com/aws/efs-utils) |
| AWS Elastic Beanstalk CLI | [aws/aws-elastic-beanstalk-cli](https://github.com/aws/aws-elastic-beanstalk-cli) |
| AWS Encryption SDK (Python) | [aws/aws-encryption-sdk-python](https://github.com/aws/aws-encryption-sdk-python) |
| AWS Encryption SDK CLI | [aws/aws-encryption-sdk-cli](https://github.com/aws/aws-encryption-sdk-cli) |
| AWS IoT Greengrass Core SDK (Python) | [aws/aws-greengrass-core-sdk-python](https://github.com/aws/aws-greengrass-core-sdk-python) |
| AWS IoT Device SDK (Python) | [aws/aws-iot-device-sdk-python](https://github.com/aws/aws-iot-device-sdk-python) |
| AWS ParallelCluster (enhanced version of CfnCluster) | [aws/aws-parallelcluster](https://github.com/aws/aws-parallelcluster) |
| AWS SageMaker SDK (Python) | [aws/sagemaker-python-sdk](https://github.com/aws/sagemaker-python-sdk) |
| AWS SaaS Boost | [awslabs/aws-saas-boost](https://github.com/awslabs/aws-saas-boost) |
| AWS Tools for Microsoft VSTS | [AWS Tools for Microsoft Visual Studio Team Services](https://docs.aws.amazon.com/vsts/latest/userguide/welcome.html) |
| AWS Tools for PowerShell | [AWS Tools for PowerShell](https://aws.amazon.com/powershell/) |
| AWS Tools and sample code provided by AWS Premium Support | [awslabs/aws-support-tools](https://github.com/awslabs/aws-support-tools) |
| AWS Trusted Advisor Tools | [aws/Trusted-Advisor-Tools](https://github.com/aws/Trusted-Advisor-Tools) |
| AWS X-Ray Daemon | [aws/aws-xray-daemon](https://github.com/aws/aws-xray-daemon) |
| awscii - render predefined AWS graphs in ASCII art | [mhlabs/awscii-cli](https://github.com/mhlabs/awscii-cli) |
| AWS X-Ray SDK (Python) | [aws/aws-xray-sdk-python](https://github.com/aws/aws-xray-sdk-python) |
| bash-my-aws | [bash-my-universe/bash-my-aws](https://github.com/bash-my-universe/bash-my-aws.git) |
| coldsnap - command-line tool that uses the EBS direct APIs to upload and download snapshots | [awslabs/coldsnap](https://github.com/awslabs/coldsnap) |
| Neptune Graph Notebook (Python) | [aws/graph-notebook](https://github.com/aws/graph-notebook) |
| kubectl | [kubernetes/kubectl](https://github.com/kubernetes/kubectl) |

## Security

| Description | Repo/Link |
| :--- | :--- |
| AWS Exposable Resources | [SummitRoute/aws_exposable_resources](https://github.com/SummitRoute/aws_exposable_resources) |
| AWS Security Documentation by Category | [docs.aws.amazon.com/security](https://docs.aws.amazon.com/security/)|
| AWS Security Reference Architecture (AWS SRA) | [docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/](https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/architecture.html) |
| A Secure Cloud - Repository of customizable AWS security configurations and best practices | [asecure.cloud/](https://asecure.cloud/) |
| Open source tools for AWS security | [toniblyx/my-arsenal-of-aws-security-tools](https://github.com/toniblyx/my-arsenal-of-aws-security-tools) |
| AWS IAM Policy Simulator | [IAM Policy Simulator Console](https://policysim.aws.amazon.com/) |
| AWS Managed Policies (list/monitor) | [z0ph/aws_managed_policies](https://github.com/z0ph/aws_managed_policies/tree/master/policies) |
| AWS Policy Generator | [AWS Policy Generator](https://awspolicygen.s3.amazonaws.com/policygen.html) |
| AWS Security Benchmark | [awslabs/aws-security-benchmark](https://github.com/awslabs/aws-security-benchmark) |
| AWS Security Hub Multiaccount Scripts | [awslabs/aws-securityhub-multiaccount-scripts](https://github.com/awslabs/aws-securityhub-multiaccount-scripts) |
| AWS Shield Engagement Lambda | https://s3.amazonaws.com/aws-shield-lambda/ShieldEngagementLambda.pdf |
| AWS WAF Security Automations | [awslabs/aws-waf-security-automations](https://github.com/awslabs/aws-waf-security-automations) |
| Automated Incident Response with SSM | [aws-samples/automated-incident-response-with-ssm](https://github.com/aws-samples/automated-incident-response-with-ssm) |
| Import AWS Config Findings into AWS Security Hub | [aws-samples/aws-securityhub-config-integration](https://github.com/aws-samples/aws-securityhub-config-integration) |
| amazon-detective-multiaccount-scripts | [aws-samples/amazon-detective-multiaccount-scripts](https://github.com/aws-samples/amazon-detective-multiaccount-scripts) |
| AWS Self-Service Security Assessment tool | [awslabs/aws-security-assessment-solution](https://github.com/awslabs/aws-security-assessment-solution)|
| aws-securityhub-to-email | [aws-samples/aws-securityhub-to-email](https://github.com/aws-samples/aws-securityhub-to-email) |
| aws-securityhub-to-slack | [aws-samples/aws-securityhub-to-slack](https://github.com/aws-samples/aws-securityhub-to-slack) |
| cloud-custodian | [cloud-custodian/cloud-custodian](https://github.com/cloud-custodian/cloud-custodian) |
| CloudGoat | [RhinoSecurityLabs/cloudgoat](https://github.com/RhinoSecurityLabs/cloudgoat) |
| git-secrets | [awslabs/git-secrets](https://github.com/awslabs/git-secrets) |
| Pacu an open source AWS exploitation framework | [RhinoSecurityLabs/Pacu](https://github.com/RhinoSecurityLabs/pacu) |
| Redboto | [elitest/Redboto](https://github.com/elitest/Redboto) |
| Endgame: Creating Backdoors in AWS | [hirajanwin/endgame](https://github.com/hirajanwin/endgame) |
| Endgame: AWS Pentesting tool | [DavidDikker/endgame](https://github.com/DavidDikker/endgame) |

## Chaos Engineering

| Description | Repo/Link |
| :--- | :--- |
| AWS SSM Chaos Runner | [amzn/awsssmchaosrunner](https://github.com/amzn/awsssmchaosrunner) |
| Chaos Injection for AWS resources using Amazon SSM Run Command and Automation | [adhorn/chaos-ssm-documents](https://github.com/adhorn/chaos-ssm-documents) |

### Networking

| Description | Repo/Link |
| :--- | :--- |
| AWS CIDR Finder | [aws-samples/aws-cidr-finder](https://github.com/aws-samples/aws-cidr-finder) |
| AWS IP Ranges | [aws-samples/awsipranges](https://github.com/aws-samples/awsipranges) |
| AWS Network Firewall CFN templates | [aws-samples/aws-networkfirewall-cfn-templates](https://github.com/aws-samples/aws-networkfirewall-cfn-templates) |
| [Serverless Transit Network Orchestrator](https://aws.amazon.com/solutions/serverless-transit-network-orchestrator/) | [awslabs/serverless-transit-network-orchestrator](https://github.com/awslabs/serverless-transit-network-orchestrator) |
| TGW (Transit Gateway) Migrator Tool | [TGW Migrator Tool](https://aws.amazon.com/blogs/networking-and-content-delivery/migrate-from-transit-vpc-to-aws-transit-gateway/) |
| TGW Route Limits Monitoring | [aws-samples/how-to-monitor-tgw-route-limits-using-serverless-architecture](https://github.com/aws-samples/how-to-monitor-tgw-route-limits-using-serverless-architecture) |
| TGW to solve overlapping CIDRs | [aws-samples/aws-transit-gateway-overlapping-cidrs](https://github.com/aws-samples/aws-transit-gateway-overlapping-cidrs) |

### Closing account

| Description | Repo/Link |
| :--- | :--- |
| How do I close my AWS account? | [How do I close my AWS account?](https://aws.amazon.com/premiumsupport/knowledge-center/close-aws-account/) |
| aws-nuke Remove all resources from an AWS account | [rebuy-de/aws-nuke](https://github.com/rebuy-de/aws-nuke) |

## Other AWS useful tools

| Description | Repo/Link |
| :--- | :--- |
| Amazon DynamoDB NoSQL Workbench | [NoSQL Workbench for Amazon DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/workbench.html) |
| Amazon Honeycode | [builder.honeycode.aws](https://builder.honeycode.aws/) |
| AWS Auto Scaling Custom Resources | [aws/aws-auto-scaling-custom-resource](https://github.com/aws/aws-auto-scaling-custom-resource) |
| AWS Deployment Framework (ADF) | [awslabs/aws-deployment-framework](https://github.com/awslabs/aws-deployment-framework) |
| AWS Distributed Load Testing | [awslabs/distributed-load-testing-on-aws](https://github.com/awslabs/distributed-load-testing-on-aws) |
| AWS Glue ETL Code Samples | [aws-samples/aws-glue-samples](https://github.com/aws-samples/aws-glue-samples) |
| AWS Glue Libs | [awslabs/aws-glue-libs](https://github.com/awslabs/aws-glue-libs) |
| AWS Instance Scheduler | [AWS Instance Scheduler](https://aws.amazon.com/solutions/instance-scheduler/) |
| AWS Multi Account Viewer | [awslabs/aws-multi-account-viewer](https://github.com/awslabs/aws-multi-account-viewer) |
| AWS Perspective | [awslabs/aws-perspective](https://github.com/awslabs/aws-perspective) |
| AWS Proton Sample Templates | [aws-samples/aws-proton-sample-templates](https://github.com/aws-samples/aws-proton-sample-templates) |
| AWS Proton Sample Fargate Templates | [aws-samples/aws-proton-sample-fargate-service](https://github.com/aws-samples/aws-proton-sample-fargate-service) |
| awslimitchecker | [jantman/awslimitchecker](https://github.com/jantman/awslimitchecker) |

## Data sources

| Description | Repo/Link |
| :--- | :--- |
| Registry of Open Data on AWS | [registry.opendata.aws](https://registry.opendata.aws/) |
| Landset 8 satellite imagery of all land on Earth | [registry.opendata.aws/landsat-8](https://registry.opendata.aws/landsat-8/), <br/> [landsatonaws.com](https://landsatonaws.com/)|

## Other tools

| Description | Repo/Link |
| :--- | :--- |
| CNCF Cloud Native Interactive Landscape | [landscape.cncf.io](https://landscape.cncf.io/) |
| Awesome Hacking | [Hack-with-Github/Awesome-Hacking](https://github.com/Hack-with-Github/Awesome-Hacking)|
| FastAPI | [tiangolo/fastapi](https://github.com/tiangolo/fastapi) |
| OpenFaaS | [openfaas/faas](https://github.com/openfaas/faas) |
| Regex tester and debugger: PHP, PCRE, Python, Golang and JavaScript | [regex101.com](https://regex101.com/) |
| Subnet Calculator - MxToolbox | [mxtoolbox.com](https://mxtoolbox.com/subnetcalculator.aspx) |

## Best Practices Guides

- [AWS Well-Architected Framework - Operational Excellence](https://wa.aws.amazon.com/wat.pillar.operationalExcellence.en.html), AWS
- [Security Overview of AWS Lambda: An In-Depth Look at AWS Lambda Security](https://d1.awsstatic.com/whitepapers/Overview-AWS-Lambda-Security.pdf), AWS, JAN 2021
- [Amazon EKS Best Practices Guide for Security](https://aws.github.io/aws-eks-best-practices/), AWS
- [Best practices for working with Amazon Aurora Serverless](https://aws.amazon.com/blogs/database/best-practices-for-working-with-amazon-aurora-serverless/), AWS, 27 NOV 2020
- [Tagging Best Practices](https://d1.awsstatic.com/whitepapers/aws-tagging-best-practices.pdf), AWS, DEC 2018

## Workshops

- [workshops.aws](https://workshops.aws/)
- [Amplify Days ANZ](https://amplifydays.awsanz.com/)
- [App Mesh Workshop](https://www.appmeshworkshop.com/)
- [Asynchronous Messaging Workshop](https://github.com/aws-samples/asynchronous-messaging-workshop/)
- [CDK Workshop](https://cdkworkshop.com/)
- [CI/CD for Serverless Applications Workshops](https://cicd.serverlessworkshops.io/)
- [Networking Immersion Day](https://networking.workshop.aws/)
- [One Observability Workshop](https://observability.workshop.aws/)
- [Redshift Immersion Workshop](https://redshift-immersion.workshop.aws/)
- [Serverless applications with streaming data](https://github.com/aws-samples/serverless-streaming-data-application/tree/main)
- [Serverless Security Workshop](https://github.com/aws-samples/aws-serverless-security-workshop/)
- [Service Catalog Tools Workshop](https://service-catalog-tools-workshop.com/)
- [Spot Instances Workshops](https://ec2spotworkshops.com/)
- [Spot Instances with EKS Workshops](https://ec2spotworkshops.com/using_ec2_spot_instances_with_eks.html)
- [VPC Endpoint Workshop](https://www.vpcendpointworkshop.com/)
- [Well-Architected Labs](https://wellarchitectedlabs.com/)

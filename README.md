# aws-tools

[![githubactions](https://github.com/kyhau/aws-tools/workflows/Build-Test/badge.svg)](https://github.com/kyhau/aws-tools/actions)
[![travisci](https://travis-ci.org/kyhau/aws-tools.svg?branch=master)](https://travis-ci.org/kyhau/aws-tools)
[![codecov](https://codecov.io/gh/kyhau/aws-tools/branch/main/graph/badge.svg)](https://codecov.io/gh/kyhau/aws-tools)

This repo provides some tools and sample code I created for building with AWS.

---
## For running Python scripts

Most of the Python scripts support multi accounts and regions.

Python 3.7 +

```
# Create and activate virtual env (optional)
virtualenv env -p python3.9
. env/bin/activate

# Install the required packages
pip install -r requirements.txt

# Optional
source .aliases
```

## For running CLI tools and shell scripts

```
pip install -r requirements-cli.txt
```

---
## Quick links for news, blogs and resources

- [What's New with AWS?](https://aws.amazon.com/new/?nc2=h_ql_exm&whats-new-content-all.sort-by=item.additionalFields.postDateTime&whats-new-content-all.sort-order=desc&wn-featured-announcements.sort-by=item.additionalFields.numericSort&wn-featured-announcements.sort-order=asc) | feed https://aws.amazon.com/blogs/aws/feed/
- [AWS Architecture Blog](https://aws.amazon.com/blogs/architecture)
- [Amazon Serverless Land Blogs](https://serverlessland.com/blog)
- [AWS re:Post](https://repost.aws/)
- [Amazon Builder's Library](https://aws.amazon.com/builders-library)
- [Cloud Pegboard](https://cloudpegboard.com/detail.html)
- [AWS Edge Chat](https://soundcloud.com/awsedgechat)

---
## Some Notes

- [Amplify](./Amplify/)
- [APIGateway](./APIGateway/)
- [AppSync](./AppSync/)
- [Athena](./Athena/)
- [AutoScaling](./AutoScaling.md)
- [AWS-Tools](./AWS-Tools/)
- [Bottlerocket](./Bottlerocket/)
- [CDK](./CDK/)
- [CloudFormation](./CloudFormation/)
- [CloudFront-S3](./CloudFront-S3/)
- [CloudShell](./CloudShell/)
- [CloudWatch](./CloudWatch/)
- [CodeArtifact](./CodeArtifact/)
- [CodeStar, CodePipeline](./CodeStar-CodePipeline/)
- [Cognito](./Cognito/)
- [Config](./Config/)
- [DynamoDB](./DynamoDB/)
- [EB](./EB/)
- [EBS, EFS](./EBS-EFS.md)
- [EC2](./EC2/)
- [EC2 Image Builder](./EC2-ImageBuilder/)
- [ECR](./ECR/)
- [ECS](./ECS/)
- [ECS vs. EKS](./ECS-vs-EKS.md)
- [EKS](./EKS/)
- [ELB](./ELB/)
- [EMR](./EMR/)
- [FirewallManager](./WAF-FirewallManager-Shield/)
- [Glue](./Glue.md)
- [Graviton](./Graviton.md)
- [Lambda](./Lambda/)
- [Kinesis](./Kinesis/)
- [MSK](./MSK/)
- [Neptune](./Neptune/)
- [OpenSearch (prev. ElasticSearch Service)](./OpenSearch/)
- [Organizations](./Organizations/)
- [RDS](./RDS/)
- [Redshift](./Redshift/)
- [Route 53](./Route53/)
- [SageMaker](./SageMaker/)
- [SAM, Serverless Application Registry](./SAM-and-ServerlessApplicationRepository/)
- [SecurityHub](./SecurityHub/)
- [Shield](./WAF-FirewallManager-Shield/)
- [SQS](./SQS/)
- [SSM](./SSM/)
- [StepFunctions](./StepFunctions/)
- [STS](./STS/)
- [TrustedAdvisor](./TrustedAdvisor/)
- [VPC](./VPC/)
- [VPC Endpoint](./VPC-Endpoint/)
- [WAF, Firewall Manager, Shield](./WAF-FirewallManager-Shield/)
- [X-Ray](./X-Ray/)

Some Specific Topics

- [App Mesh](./AppMesh.md)
- [Chaos Engineering](./Others/ChaosEngineering.md)
- [Closing Account](./Others/ClosingAccount.md)
- [ECS vs. EKS](./ECS-vs-EKS.md)
- [Data Sources](./Others/DataSources.md)
- [Encryption](./Others/Encryption.md)
- [Networking](./Networking/)
- [Other useful tools](./Others/)
- [Security](./Security.md)
- [Serverless](./Serverless.md)
- [Service Limits](./Others/ServiceLimits.md)
- [Visualisation](https://github.com/kyhau/aws-resource-visualisation/)

Other Notes

- [My AWS Certification Notes (kyhau/aws-notebook)](https://github.com/kyhau/aws-notebook)

Other AWS related tools

- AWS CLI interactive productivity booster (aws-shell) [awslabs/aws-shell](https://github.com/awslabs/aws-shell)
- AWS Cloud Digital Interface (CDI) Software Development Kit (SDK) is a set of libraries and documentation for you to build - AWS Deployment Framework (ADF) [awslabs/aws-deployment-framework](https://github.com/awslabs/aws-deployment-framework)
- AWS Distributed Load Testing - [awslabs/distributed-load-testing-on-aws](https://github.com/awslabs/distributed-load-testing-on-aws)
- AWS IoT Greengrass Core SDK (Python) [aws/aws-greengrass-core-sdk-python](https://github.com/aws/aws-greengrass-core-sdk-python)
- AWS IoT Device SDK (Python) [aws/aws-iot-device-sdk-python](https://github.com/aws/aws-iot-device-sdk-python)
- AWS ParallelCluster (enhanced version of CfnCluster) [aws/aws-parallelcluster](https://github.com/aws/aws-parallelcluster)
- AWS Proton Sample Templates - [aws-samples/aws-proton-sample-templates](https://github.com/aws-samples/aws-proton-sample-templates)
- AWS Proton Sample Fargate Templates - [aws-samples/aws-proton-sample-fargate-service](https://github.com/aws-samples/aws-proton-sample-fargate-service)
- AWS SaaS Boost - [awslabs/aws-saas-boost](https://github.com/awslabs/aws-saas-boost)
- Amazon Honeycode - [builder.honeycode.aws](https://builder.honeycode.aws/)
- Amazon Ion Python - [amzn/ion-python](https://github.com/amzn/ion-python)
- AutoML Toolkit for Deep Learning - [awslabs/autogluon](https://github.com/awslabs/autogluon)
live video solutions on AWS - [aws/aws-cdi-sdk](https://github.com/aws/aws-cdi-sdk)
- awscii - render predefined AWS graphs in ASCII art - [mhlabs/awscii-cli](https://github.com/mhlabs/awscii-cli)
- bash-my-aws - [bash-my-universe/bash-my-aws](https://github.com/bash-my-universe/bash-my-aws.git)

Other tools

- CNCF Cloud Native Interactive Landscape - [landscape.cncf.io](https://landscape.cncf.io/)
- Awesome Hacking - [Hack-with-Github/Awesome-Hacking](https://github.com/Hack-with-Github/Awesome-Hacking)-
- FastAPI - [tiangolo/fastapi](https://github.com/tiangolo/fastapi)
- OpenFaaS - [openfaas/faas](https://github.com/openfaas/faas)
- Regex tester and debugger: PHP, PCRE, Python, Golang and JavaScript - [regex101.com](https://regex101.com/)
- Subnet Calculator - MxToolbox - [mxtoolbox.com](https://mxtoolbox.com/subnetcalculator.aspx)

Data Sources

- Registry of Open Data on AWS - [registry.opendata.aws](https://registry.opendata.aws/)
- Landset 8 satellite imagery of all land on Earth - [registry.opendata.aws/landsat-8](https://registry.opendata.aws/landsat-8/), [landsatonaws.com](https://landsatonaws.com/)


Best Practices Guides

- [AWS Well-Architected Framework - Operational Excellence](https://wa.aws.amazon.com/wat.pillar.operationalExcellence.en.html), AWS
- [Amazon EKS Best Practices Guide for Security](https://aws.github.io/aws-eks-best-practices/), AWS
- [AWS Security Reference Architecture (AWS SRA)](https://d1.awsstatic.com/APG/aws-security-reference-architecture.pdf), AWS, JUN 2021
- [Security Overview of AWS Lambda: An In-Depth Look at AWS Lambda Security](https://d1.awsstatic.com/whitepapers/Overview-AWS-Lambda-Security.pdf), AWS, JAN 2021
- [Best practices for working with Amazon Aurora Serverless](https://aws.amazon.com/blogs/database/best-practices-for-working-with-amazon-aurora-serverless/), AWS, 27 NOV 2020
- [Tagging Best Practices](https://d1.awsstatic.com/whitepapers/aws-tagging-best-practices.pdf), AWS, DEC 2018


Workshops

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

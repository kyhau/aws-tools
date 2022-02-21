# aws-tools

[![githubactions](https://github.com/kyhau/aws-tools/workflows/Build-Test/badge.svg)](https://github.com/kyhau/aws-tools/actions)
[![travisci](https://travis-ci.org/kyhau/aws-tools.svg?branch=master)](https://travis-ci.org/kyhau/aws-tools)
[![codecov](https://codecov.io/gh/kyhau/aws-tools/branch/master/graph/badge.svg)](https://codecov.io/gh/kyhau/aws-tools)

This repo provides some tools and sample code I created for building with AWS.

## For running Python scripts

Most of the Python scripts support multi accounts and regions.

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
## Some Notes

- [Amplify](./Amplify/README.md)
- [APIGateway](./APIGateway/README.md)
- [Athena](./Athena/README.md)
- [AutoScaling](./AutoScaling.md)
- [AWS-Tools](./AWS-Tools/README.md)
- [CDK](./CDK/README.md)
- [CloudFormation](./CloudFormation/README.md)
- [CloudFront-S3](./CloudFront-S3/README.md)
- [CloudShell](./CloudShell/README.md)
- [CloudWatch](./CloudWatch/README.md)
- [CodeArtifact](./CodeArtifact/README.md)
- [CodeStar, CodePipeline](./CodeStar-CodePipeline/README.md)
- [Cognito](./Cognito/README.md)
- [Config](./Config/README.md)
- [DynamoDB](./DynamoDB/README.md)
- [EB](./EB/README.md)
- [EBS, EFS](./EBS-EFS.md)
- [EC2](./EC2/README.md)
- [EC2 Image Builder](./EC2-ImageBuilder/README.md)
- [ECR](./ECR/README.md)
- [ECS](./ECS/README.md)
- [EKS](./EKS/README.md)
- [ELB](./ELB/)
- [EMR](./EMR/)
- [FirewallManager](./FirewallManager.md)
- [Glue](./Glue.md)
- [Kinesis](./Kinesis/README.md)
- [SecurityHub](./SecurityHub/README.md)
- [SQS](./SQS/README.md)
- [SSM](./SSM/README.md)
- [StepFunctions](./StepFunctions/README.md)
- [STS](./STS/README.md)
- [TrustedAdvisor](./TrustedAdvisor/README.md)
- [VPC Endpoint](./VPC-Endpoint/README.md)
- [X-Ray](./X-Ray/README.md)

Some Specific Topics

- [App Mesh](./AppMesh.md)
- [Chaos Engineering](./Useful-tools/ChaosEngineering.md)
- [Closing Account](./Useful-tools/ClosingAccount.md)
- [Data Sources](./Useful-tools/DataSources.md)
- [Encryption](./Useful-tools/Encryption.md)
- [Networking](./Networking/README.md)
- [Security](./Security.md)
- [Serverless](./Serverless.md)
- [Service Limits](./Useful-tools/ServiceLimits.md)
- [Useful tools](./Useful-tools/)
- [Visualisation](https://github.com/kyhau/aws-resource-visualisation/)

Other Notes

- [My AWS Certification Notes (kyhau/aws-notebook)](https://github.com/kyhau/aws-notebook)

Other AWS related tools

- AWS CLI interactive productivity booster (aws-shell) [awslabs/aws-shell](https://github.com/awslabs/aws-shell)
- AWS Cloud Digital Interface (CDI) Software Development Kit (SDK) is a set of libraries and documentation for you to build - AWS Deployment Framework (ADF) [awslabs/aws-deployment-framework](https://github.com/awslabs/aws-deployment-framework)
- AWS Distributed Load Testing - [awslabs/distributed-load-testing-on-aws](https://github.com/awslabs/
- AWS IoT Greengrass Core SDK (Python) [aws/aws-greengrass-core-sdk-python](https://github.com/aws/aws-greengrass-core-sdk-python)
- AWS IoT Device SDK (Python) [aws/aws-iot-device-sdk-python](https://github.com/aws/aws-iot-device-sdk-python)
- AWS ParallelCluster (enhanced version of CfnCluster) [aws/aws-parallelcluster](https://github.com/aws/aws-parallelcluster)
- AWS Proton Sample Templates - [aws-samples/aws-proton-sample-templates](https://github.com/aws-samples/aws-proton-sample-templates)
- AWS Proton Sample Fargate Templates - [aws-samples/aws-proton-sample-fargate-service](https://github.com/aws-samples/aws-proton-sample-fargate-service)
- AWS SaaS Boost - [awslabs/aws-saas-boost](https://github.com/awslabs/aws-saas-boost)
- Amazon Honeycode - [builder.honeycode.aws](https://builder.honeycode.aws/)
distributed-load-testing-on-aws)
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

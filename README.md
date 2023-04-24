# aws-tools

[![githubactions](https://github.com/kyhau/aws-tools/workflows/Build-Test/badge.svg)](https://github.com/kyhau/aws-tools/actions/workflows/build-test-common-helper.yaml)
[![githubactions](https://github.com/kyhau/aws-tools/workflows/Lint/badge.svg)](https://github.com/kyhau/aws-tools/actions/workflows/lint.yaml)
[![codecov](https://codecov.io/gh/kyhau/aws-tools/branch/main/graph/badge.svg)](https://codecov.io/gh/kyhau/aws-tools)
[![CodeQL](https://github.com/kyhau/aws-tools/workflows/CodeQL/badge.svg)](https://github.com/kyhau/aws-tools/actions/workflows/codeql-analysis.yml)

This repository includes some tools and sample code I created for building with AWS.

All notable changes to this project will be documented in [CHANGELOG](./CHANGELOG.md).

---
## Built with
- Python, Shell, PowerShell, JavaScript, TypeScript, Go, Docker
- [AWS CDK v2](https://docs.aws.amazon.com/cdk/v2/guide/home.html), [AWS SAM](https://aws.amazon.com/serverless/sam/)
- [cfn-lint](https://github.com/aws-cloudformation/cfn-lint) is used to validate CloudFormation templates in this repository.
- [CodeQL](https://codeql.github.com) is [enabled](.github/workflows/codeql-analysis.yml) in this repository.
- [Dependabot version updates](https://docs.github.com/en/code-security/dependabot/dependabot-version-updates) is [enabled](.github/dependabot.yml) in this repository.
- [Snyk](https://github.com/snyk/actions) is enabled in the GitHub Actions [workflow](.github/workflows/build-test-common-helper.yaml).

---
## AWS login

[saml2aws-multi](https://github.com/kyhau/saml2aws-multi) is my version of AWS login tool providing an easy-to-use command line interface to support login and retrieve AWS temporary credentials for multiple roles of different accounts with [saml2aws](https://github.com/Versent/saml2aws).

---
## For running Python scripts

Most of the Python scripts support processing multiple AWS accounts (via AWS profiles in ~/.aws/credentials) and AWS regions using `AwsApiHelper` in the common [helper.aws.AwsApiHelper](./_common/helper/aws.py) module.


Support Python 3.7, 3.8, 3.9, 3.10, 3.11
```
pip3 install -r requirements.txt
```
Set aliases (Optional)

```
source .aliases
```

## For running CLI tools and shell scripts

```
pip3 install -r requirements-cli.txt
```

---
## My notes
- My notes of each service is in its folder respectively.
- Some specific topics (no folder)
    - [App Mesh](./AppMesh.md)
    - [Chaos Engineering](./Others/ChaosEngineering.md)
    - [Closing Account](./Others/ClosingAccount.md)
    - [ECS vs. EKS](./ECS-vs-EKS.md)
    - [Encryption](./Others/Encryption.md)
    - [Mutual Transport Layer Security (mutual TLS or mTLS) authentication](./Security.md)
    - [Networking](./Networking/)
    - [Other useful tools](./Others/)
    - [Security](./Security.md)
    - [Serverless](./Serverless.md)
    - [Service Limits](./Others/ServiceLimits.md)
    - [Visualisation](https://github.com/kyhau/aws-resource-visualisation/)

---
## Quick links for news, blogs and resources

- [What's New with AWS?](https://aws.amazon.com/new/?nc2=h_ql_exm&whats-new-content-all.sort-by=item.additionalFields.postDateTime&whats-new-content-all.sort-order=desc&wn-featured-announcements.sort-by=item.additionalFields.numericSort&wn-featured-announcements.sort-order=asc) | feed https://aws.amazon.com/blogs/aws/feed/
- [AWS Architecture Blog](https://aws.amazon.com/blogs/architecture)
- [Amazon Serverless Land Blogs](https://serverlessland.com/blog)
- [AWS re:Post](https://repost.aws/)
- [Cloud Pegboard](https://cloudpegboard.com/detail.html)
- [AWS Edge Chat](https://soundcloud.com/awsedgechat)

### AWS design + build tools

- [AWS Workshops](https://workshops.aws/)
- [AWS Architecture Center](https://aws.amazon.com/architecture/?cards-all.sort-by=item.additionalFields.sortDate&cards-all.sort-order=desc&awsf.content-type=*all&awsf.methodology=*all&awsf.tech-category=*all&awsf.industries=*all&awsf.business-category=*all)
- [AWS Solutions Library](https://aws.amazon.com/solutions/)
- [Amazon Builder's Library](https://aws.amazon.com/builders-library)
- [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html) and [AWS Well-Architected Tool](https://docs.aws.amazon.com/wellarchitected/latest/userguide/intro.html)
- [Serverless Land](https://serverlessland.com/)
- [AWS Application Composer](https://aws.amazon.com/application-composer/) (Preview)

### Other AWS related tools

- AWS CLI interactive productivity booster (aws-shell) [awslabs/aws-shell](https://github.com/awslabs/aws-shell)
- AWS Cloud Digital Interface (CDI) Software Development Kit (SDK) is a set of libraries and documentation for you to build - AWS Deployment Framework (ADF) [awslabs/aws-deployment-framework](https://github.com/awslabs/aws-deployment-framework)
- AWS Distributed Load Testing - [awslabs/distributed-load-testing-on-aws](https://github.com/awslabs/distributed-load-testing-on-aws)
- AWS ParallelCluster (enhanced version of CfnCluster) [aws/aws-parallelcluster](https://github.com/aws/aws-parallelcluster)
- AWS Proton Sample Templates - [aws-samples/aws-proton-sample-templates](https://github.com/aws-samples/aws-proton-sample-templates)
- AWS Proton Sample Fargate Templates - [aws-samples/aws-proton-sample-fargate-service](https://github.com/aws-samples/aws-proton-sample-fargate-service)
- AWS SaaS Boost - [awslabs/aws-saas-boost](https://github.com/awslabs/aws-saas-boost)
- Amazon Honeycode - [builder.honeycode.aws](https://builder.honeycode.aws/)
- AutoML Toolkit for Deep Learning - [awslabs/autogluon](https://github.com/awslabs/autogluon)
live video solutions on AWS - [aws/aws-cdi-sdk](https://github.com/aws/aws-cdi-sdk)
- awscii - render predefined AWS graphs in ASCII art - [mhlabs/awscii-cli](https://github.com/mhlabs/awscii-cli)
- bash-my-aws - [bash-my-universe/bash-my-aws](https://github.com/bash-my-universe/bash-my-aws.git)

### Best Practices Guides

- [AWS Well-Architected Framework - Operational Excellence](https://wa.aws.amazon.com/wat.pillar.operationalExcellence.en.html), AWS
- [Amazon EKS Best Practices Guide for Security](https://aws.github.io/aws-eks-best-practices/), AWS
- [AWS Security Reference Architecture (AWS SRA)](https://d1.awsstatic.com/APG/aws-security-reference-architecture.pdf), AWS, JUN 2021
- [Security Overview of AWS Lambda: An In-Depth Look at AWS Lambda Security](https://d1.awsstatic.com/whitepapers/Overview-AWS-Lambda-Security.pdf), AWS, JAN 2021
- [Best practices for working with Amazon Aurora Serverless](https://aws.amazon.com/blogs/database/best-practices-for-working-with-amazon-aurora-serverless/), AWS, 27 NOV 2020
- [Tagging Best Practices](https://d1.awsstatic.com/whitepapers/aws-tagging-best-practices.pdf), AWS, DEC 2018

### Data Sources

- Registry of Open Data on AWS - [registry.opendata.aws](https://registry.opendata.aws/)
- Landset 8 satellite imagery of all land on Earth - [registry.opendata.aws/landsat-8](https://registry.opendata.aws/landsat-8/), [landsatonaws.com](https://landsatonaws.com/)

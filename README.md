# aws-tools

[![Common Helper Build](https://github.com/kyhau/aws-tools/actions/workflows/common-helper-build.yml/badge.svg)](https://github.com/kyhau/aws-tools/actions/workflows/common-helper-build.yml)
[![Lint](https://github.com/kyhau/aws-tools/actions/workflows/lint.yaml/badge.svg)](https://github.com/kyhau/aws-tools/actions/workflows/lint.yaml)
[![Codecov](https://codecov.io/gh/kyhau/aws-tools/branch/main/graph/badge.svg)](https://codecov.io/gh/kyhau/aws-tools)
[![CodeQL](https://github.com/kyhau/aws-tools/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/kyhau/aws-tools/actions/workflows/codeql-analysis.yml)
[![Secrets Scan](https://github.com/kyhau/aws-tools/actions/workflows/secrets-scan.yml/badge.svg)](https://github.com/kyhau/aws-tools/actions/workflows/secrets-scan.yml)
![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue)
![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)
![GitHub last commit](https://img.shields.io/github/last-commit/kyhau/aws-tools)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](http://en.wikipedia.org/wiki/MIT_License)

This repository includes some tools and sample code I created for building with AWS.<br>
All notable changes to this project are documented in [CHANGELOG](./CHANGELOG.md).

Jump to:
- [Built with](#built-with)
- [To run the scripts](#to-run-the-scripts)
    - [AWS Login with saml2aws-multi](#aws-login)
    - [For running Python scripts](#for-running-python-scripts)
    - [For running CLI tools and shell scripts](#for-running-cli-tools-and-shell-scripts)
- [My notes](#my-notes)
- [Quick links for news, blogs and resources](#quick-links-for-news-blogs-and-resources)

---

## Built with

### 💻 Languages & Technologies
- **Python** (3.10, 3.11, 3.12, 3.13) - Primary language for automation and tools
- **Shell** (Bash) - System scripts and automation
- **PowerShell** - Windows automation
- **JavaScript/TypeScript** - AWS Lambda functions and CDK constructs
- **Go** - High-performance CLI tools
- **Docker** - Containerization

### 🏗️ Infrastructure as Code
- [**AWS CDK v2**](https://docs.aws.amazon.com/cdk/v2/guide/home.html) - Cloud Development Kit for infrastructure
- [**AWS SAM**](https://aws.amazon.com/serverless/sam/) - Serverless Application Model
- **AWS CloudFormation** - Infrastructure templates
- [**cfn-lint**](https://github.com/aws-cloudformation/cfn-lint) - CloudFormation template validation

### 🔧 Development Tools
- [**Poetry**](https://python-poetry.org/) - Python dependency management ([_common](./_common))
- [**pytest**](https://pytest.org/) - Testing framework with coverage reporting
- [**black**](https://github.com/psf/black) - Python code formatter
- [**flake8**](https://github.com/PyCQA/flake8) - Python linting
- [**yamllint**](https://yamllint.readthedocs.io/) - YAML file linting

### 🔐 Security & Code Quality
- [**CodeQL**](https://codeql.github.com) - Automated security analysis ([workflow](.github/workflows/codeql-analysis.yml))
- [**Gitleaks**](https://github.com/gitleaks/gitleaks) & [**TruffleHog**](https://github.com/trufflesecurity/trufflehog) - Secrets scanning ([workflow](.github/workflows/secrets-scan.yml))
- [**Snyk**](https://github.com/snyk/actions) - Vulnerability scanning ([workflow](.github/workflows/common-helper-build.yml))
- [**Dependabot**](https://docs.github.com/en/code-security/dependabot) - Automated dependency updates ([config](.github/dependabot.yml))

## To run the scripts

### AWS login

- [saml2aws-multi](https://github.com/kyhau/saml2aws-multi) is my version of AWS login tool providing an easy-to-use command line interface to support login and retrieve AWS temporary credentials for multiple roles of different accounts with [saml2aws](https://github.com/Versent/saml2aws).

### For running Python scripts

- Most of the Python scripts support processing multiple AWS accounts (via AWS profiles in `~/.aws/credentials`) and AWS regions using `AwsApiHelper` in the common [helper.aws.AwsApiHelper](./_common/helper/aws.py) module.
- Automated tests run with Python 3.10, 3.11, 3.12, 3.13
- To start, install dependencies by running:
    ```
    pip3 install -r requirements.txt
    ```
- Set aliases (optional):
    ```
    source .aliases
    ```

### For running CLI tools and shell scripts

- To start, install dependencies by running:
    ```
    pip3 install -r requirements-cli.txt
    ```

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
- [Serverless Land](https://serverlessland.com/)
- [AWS Application Composer](https://aws.amazon.com/application-composer/)

### Other AWS related tools

- AWS CLI interactive productivity booster (aws-shell) [awslabs/aws-shell](https://github.com/awslabs/aws-shell)
- AWS Cloud Digital Interface (CDI) Software Development Kit (SDK) is a set of libraries and documentation for you to build - AWS Deployment Framework (ADF) [awslabs/aws-deployment-framework](https://github.com/awslabs/aws-deployment-framework)
- AWS ParallelCluster (enhanced version of CfnCluster) [aws/aws-parallelcluster](https://github.com/aws/aws-parallelcluster)
- AWS Region Comparison Tool - https://region-comparison-tool.com/
- AWS SaaS Boost - [awslabs/aws-saas-boost](https://github.com/awslabs/aws-saas-boost)
- Amazon Honeycode - [builder.honeycode.aws](https://builder.honeycode.aws/) - RETIRED
- Live video solutions on AWS - [aws/aws-cdi-sdk](https://github.com/aws/aws-cdi-sdk)
- awscii - render predefined AWS graphs in ASCII art - [mhlabs/awscii-cli](https://github.com/mhlabs/awscii-cli)
- bash-my-aws - [bash-my-universe/bash-my-aws](https://github.com/bash-my-universe/bash-my-aws.git)

### Data Sources

- Registry of Open Data on AWS - [registry.opendata.aws](https://registry.opendata.aws/)
- Landset 8 satellite imagery of all land on Earth - [registry.opendata.aws/landsat-8](https://registry.opendata.aws/landsat-8/), [landsatonaws.com](https://landsatonaws.com/)

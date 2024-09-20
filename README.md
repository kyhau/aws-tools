# aws-tools

[![githubactions](https://github.com/kyhau/aws-tools/actions/workflows/common-helper-build.yml/badge.svg)](https://github.com/kyhau/aws-tools/actions/workflows/common-helper-build.yml)
[![githubactions](https://github.com/kyhau/aws-tools/actions/workflows/lint.yaml/badge.svg)](https://github.com/kyhau/aws-tools/actions/workflows/lint.yaml)
[![codecov](https://codecov.io/gh/kyhau/aws-tools/branch/main/graph/badge.svg)](https://codecov.io/gh/kyhau/aws-tools)
[![CodeQL](https://github.com/kyhau/aws-tools/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/kyhau/aws-tools/actions/workflows/codeql-analysis.yml)
[![SecretsScan](https://github.com/kyhau/aws-tools/actions/workflows/secrets-scan.yml/badge.svg)](https://github.com/kyhau/aws-tools/actions/workflows/secrets-scan.yml)

This repository includes some tools and sample code I created for building with AWS.<br>
All notable changes to this project will be documented in [CHANGELOG](./CHANGELOG.md).

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
- Python, Shell, PowerShell, JavaScript, TypeScript, Go, Docker
- [AWS CDK v2](https://docs.aws.amazon.com/cdk/v2/guide/home.html), [AWS SAM](https://aws.amazon.com/serverless/sam/)
- [cfn-lint](https://github.com/aws-cloudformation/cfn-lint) is used for to validating CloudFormation templates.
- [CodeQL](https://codeql.github.com) is [enabled](.github/workflows/codeql-analysis.yml) in this repository.
- [Dependabot](https://docs.github.com/en/code-security/dependabot/dependabot-version-updates) is [enabled](.github/dependabot.yml) for auto dependency updates.
- [Gitleaks](https://github.com/gitleaks/gitleaks) and [TruffleHog](https://github.com/trufflesecurity/trufflehog) are enabled in this GitHub Actions [workflow](.github/workflows/secrets-scan.yml) for detecting and preventing hardcoded secrets.
- [Snyk](https://github.com/snyk/actions) is enabled in this GitHub Actions [workflow](.github/workflows/common-helper-build.yml) for vulnerability scanning and auto pull-request

## To run the scripts

### AWS login

- [saml2aws-multi](https://github.com/kyhau/saml2aws-multi) is my version of AWS login tool providing an easy-to-use command line interface to support login and retrieve AWS temporary credentials for multiple roles of different accounts with [saml2aws](https://github.com/Versent/saml2aws).

### For running Python scripts

- Most of the Python scripts support processing multiple AWS accounts (via AWS profiles in `~/.aws/credentials`) and AWS regions using `AwsApiHelper` in the common [helper.aws.AwsApiHelper](./_common/helper/aws.py) module.
- Tested with Python 3.10, 3.11, 3.12
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

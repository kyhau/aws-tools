# AWS Cloud Development Kit (CDK)

### Useful links

- [Getting Started Guide](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html)
- [github.com/aws/aws-cdk](https://github.com/aws/aws-cdk)
- [AWS CDK API Reference](https://docs.aws.amazon.com/cdk/api/latest/docs/aws-construct-library.html)
- [jsii](https://github.com/aws/jsii) allows code in any language to naturally interact with JavaScript classes.
  It is the technology that enables the AWS CDK to deliver polyglot libraries from a single codebase.
- [CDK Assume Role Credential Plugin](https://aws.amazon.com/blogs/devops/cdk-credential-plugin/)
- [aws-samples/cdk-assume-role-credential-plugin](https://github.com/aws-samples/cdk-assume-role-credential-plugin) |
- [cdk-patterns/serverless](https://github.com/cdk-patterns/serverless) |


### My small examples for demo

- https://github.com/kyhau/have-a-smile
- https://github.com/kyhau/cdk-lambda-layer-datetimenow
- https://github.com/kyhau/cdk-url-shortener-demo


---
### Quick start
```
# List the available template types & languages
cdk init --list

# Start a new CDK project (app or library)
cdk init --language python

# E.g. Install package for S3
pip install aws-cdk.aws-s3

# Access the online documentation
cdk docs

# List stacks in an application
cdk list
cdk ls

# Synthesize a CDK app to CloudFormation template(s)
cdk synthesize
cdk synth

# Diff stacks against current state
cdk diff

# Deploy a stack into an AWS account
cdk deploy

# Deletes a stack from an AWS account
cdk destroy

# Deploy a toolkit stack to support deploying large stacks & artifacts
cdk bootstrap

# Inspect the environment and produce information useful for troubleshooting
cdk doctor
```
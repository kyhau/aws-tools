# AWS Cloud Development Kit (CDK)

- [Getting Started Guide](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html)
- [**`aws-cdk`**](https://github.com/aws/aws-cdk)
- [**`jsii`**](https://github.com/aws/jsii) allows code in any language to naturally interact with JavaScript classes.
  It is the technology that enables the AWS CDK to deliver polyglot libraries from a single codebase.

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
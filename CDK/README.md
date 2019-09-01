# CDK

- https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html
- https://github.com/aws/aws-cdk/tree/master/packages/aws-cdk

```
# List the available template types & languages
cdk init --list

# Start a new CDK project (app or library)
cdk init --language python



python3 -m venv .env
source .env/bin/activate

pip install -r requirements.txt

# Change the instantiation of HelloCdkStack in app.py to the following.
#HelloCdkStack(app, "HelloCdkStack")

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
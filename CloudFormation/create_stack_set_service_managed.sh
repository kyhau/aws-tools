#!/bin/bash
# https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-getting-started-create.html

template="https://s3.amazonaws.com/cloudformation-stackset-sample-templates-us-east-1/EnableAWSConfig.yml"


aws cloudformation create-stack-set --stack-set-name StackSet_myApp --template-url ${template} --permission-model SERVICE_MANAGED --auto-deployment Enabled=true,RetainStacksOnAccountRemoval=true

aws cloudformation list-stack-sets

aws cloudformation create-stack-instances --stack-set-name StackSet_myApp --deployment-targets OrganizationalUnitIds=["ou-rcuk-1x5j1lwo", "ou-rcuk-slr5lh0a"] --regions ["eu-west-1"]

# Wait until an operation is complete before starting another one. You can run only one operation at a time.

aws cloudformation describe-stack-set-operation --stack-set-name my-awsconfig-stackset --operation-id operation_ID

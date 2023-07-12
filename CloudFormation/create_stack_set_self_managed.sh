#!/bin/bash
# https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-getting-started-create.html


template="https://s3.amazonaws.com/cloudformation-stackset-sample-templates-us-east-1/EnableAWSConfig.yml"


aws cloudformation create-stack-set --stack-set-name my-awsconfig-stackset --template-url ${template}

aws cloudformation list-stack-sets

aws cloudformation create-stack-instances --stack-set-name my-awsconfig-stackset --accounts '["account_ID_1","account_ID_2"]' --regions '["region_1","region_2"]' --operation-preferences FailureToleranceCount=0,MaxConcurrentCount=1

# Wait until an operation is complete before starting another one. You can run only one operation at a time.

aws cloudformation describe-stack-set-operation --stack-set-name my-awsconfig-stackset --operation-id operation_ID

#!/bin/bash

# 1. Get the list of all IAM Policies in the AWS account
# 2. Find the ones with an ARN containing iam::aws, so that only the AWS managed policies are grabbed.
# 3. Get the ARN, current version id, and policy name (needed so we don't have a slash as the ARN does for writing a file)
# 4. Call aws iam get-policy-version with those values, and writes the output to a file using the policy name.
# Reference: https://github.com/z0ph/aws_managed_policies

aws iam list-policies > list-policies.json

mkdir -p policies/
cat list-policies.json | jq -cr '.Policies[] | select(.Arn | contains("iam::aws"))|.Arn +" "+ .DefaultVersionId+" "+.PolicyName' | xargs -n3 sh -c 'aws iam get-policy-version --policy-arn $1 --version-id $2 > "policies/$3.json"' sh

rm list-policies.json

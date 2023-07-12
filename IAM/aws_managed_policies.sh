#!/bin/bash
# Retrieve all AWS Managed IAM policies
# See also https://github.com/SummitRoute/aws_managed_policies

# Set to fail script if any command fails.
set -e
function finish {
  [[ -f list-policies.json ]] && rm list-policies.json
}
trap finish EXIT

rm -rf "aws_managed_policies"
mkdir -p "aws_managed_policies"

aws iam list-policies > list-policies.json

(jq -cr '.Policies[] | select(.Arn | contains("iam::aws"))|.Arn +" "+ .DefaultVersionId+" "+.PolicyName' | \
 xargs -n3 sh -c 'aws iam get-policy-version --policy-arn $0 --version-id $1 > aws_managed_policies/$2.json') \
< list-policies.json

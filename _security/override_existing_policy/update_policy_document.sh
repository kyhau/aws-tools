#!/bin/bash

# Required iam:CreatePolicyVersion

POLICY_ARN="arn:aws:iam::012345678987:policy/ec2_ip_policy"

cat > newpolicyversion.json << EOL
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "*",
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOL

aws iam create-policy-version \
  --policy-arn "$POLICY_ARN" \
  --policy-document file://newpolicyversion.json \
  --set-as-default

rm newpolicyversion.json
#!/bin/bash
set -e
# https://docs.aws.amazon.com/codeartifact/latest/ug/domain-policies.html#domain-policy-example-with-aws-organizations

source .env

ORG_ID=$(aws organizations describe-organization | jq -r '.[] | .Id')

cat > policy.json << EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "DomainPolicyForOrganization",
            "Action": [
                "codeartifact:GetDomainPermissionsPolicy",
                "codeartifact:ListRepositoriesInDomain",
                "codeartifact:GetAuthorizationToken",
                "codeartifact:DescribeDomain",
                "codeartifact:CreateRepository"
            ],
            "Effect": "Allow",
            "Principal": "*",
            "Resource": "*",
            "Condition": {
                "StringEquals": { "aws:PrincipalOrgID":["${ORG_ID}"]}
            }
        }
    ]
}
EOF

aws codeartifact put-domain-permissions-policy --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} \
  --policy-document file://policy.json --profile ${AWS_PROFILE_1}

rm policy.json

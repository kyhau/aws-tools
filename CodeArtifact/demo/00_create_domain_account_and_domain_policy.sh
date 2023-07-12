#!/bin/bash
set -e
# https://docs.aws.amazon.com/codeartifact/latest/ug/domains.html

source .env

# Domain names only need to be unique within an account

aws codeartifact create-domain --domain ${DOMAIN} --profile ${AWS_PROFILE_1}

aws codeartifact list-domains --profile ${AWS_PROFILE_1}

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
                "StringEquals": {"aws:PrincipalOrgID":["${ORG_ID}"]}
            }
        }
    ]
}
EOF

aws codeartifact put-domain-permissions-policy --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} \
  --policy-document file://policy.json --profile ${AWS_PROFILE_1}

rm policy.json

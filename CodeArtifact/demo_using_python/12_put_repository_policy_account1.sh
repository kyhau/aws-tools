#!/bin/bash
set -e
# https://docs.aws.amazon.com/codeartifact/latest/ug/repo-policies.html

source .env

# Create a cross account domain policy for account 1
# copy-package-versions requires codeartifact:ReadFromRepository

cat > policy.json << EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "ContributorPolicy",
            "Action": [
                "codeartifact:AssociateWithDownstreamRepository",
                "codeartifact:CreateRepository",
                "codeartifact:DescribeDomain",
                "codeartifact:GetAuthorizationToken",
                "codeartifact:GetDomainPermissionsPolicy",
                "codeartifact:ListRepositoriesInDomain",
                "codeartifact:ReadFromRepository",
                "sts:GetServiceBearerToken"
            ],
            "Effect": "Allow",
            "Resource": "*",
            "Principal": {
                "AWS": "arn:aws:iam::${ACCOUNT_2_ID}:root"
            }
        }
    ]
}
EOF


aws codeartifact put-repository-permissions-policy --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} \
  --repository ${ACCOUNT_1_SHARED_REPO_1} --policy-document file://policy.json --profile ${AWS_PROFILE_1}

rm policy.json
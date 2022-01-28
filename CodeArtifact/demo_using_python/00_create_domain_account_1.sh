#!/bin/bash
# https://docs.aws.amazon.com/codeartifact/latest/ug/domains.html

source .config

# Domain names only need to be unique within an account

aws codeartifact create-domain --domain ${DOMAIN} --profile ${AWS_PROFILE_1}


# Create a cross account domain policy for account 1
# copy-package-versions requires codeartifact:ReadFromRepository

cat > cross_account_domain_policy.json << EOF
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


aws codeartifact put-domain-permissions-policy --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} \
  --policy-document file://cross_account_domain_policy.json --profile ${AWS_PROFILE_1}

rm cross_account_domain_policy.json
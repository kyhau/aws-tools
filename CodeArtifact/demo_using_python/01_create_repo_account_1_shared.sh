#!/bin/bash

source .config


aws codeartifact create-repository --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} \
  --repository ${ACCOUNT_1_SHARED_REPO_1} --description "My new repository" --profile ${AWS_PROFILE_1}

#aws codeartifact update-repository --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} \
#  --repository ${ACCOUNT_1_SHARED_REPO_1} --upstreams repositoryName=pypi-store --profile ${AWS_PROFILE_1}

cat > readwrite_repository_policy.json << EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "codeartifact:AssociateExternalConnection",
                "codeartifact:DescribePackageVersion",
                "codeartifact:DescribeRepository",
                "codeartifact:GetPackageVersionReadme",
                "codeartifact:GetRepositoryEndpoint",
                "codeartifact:ListPackageVersionAssets",
                "codeartifact:ListPackageVersionDependencies",
                "codeartifact:ListPackageVersions",
                "codeartifact:ListPackages",
                "codeartifact:PublishPackageVersion",
                "codeartifact:PutPackageMetadata",
                "codeartifact:ReadFromRepository"
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
  --repository ${ACCOUNT_1_SHARED_REPO_1} --policy-document file://readwrite_repository_policy.json --profile ${AWS_PROFILE_1}

rm readwrite_repository_policy.json

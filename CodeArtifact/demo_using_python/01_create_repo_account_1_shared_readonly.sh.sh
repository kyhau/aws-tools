#!/bin/bash

source .config


aws codeartifact create-repository --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} \
  --repository ${ACCOUNT_1_SHARED_REPO_2} --description "My new repository" --profile ${AWS_PROFILE_1}

#aws codeartifact update-repository --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} \
# --repository ${ACCOUNT_1_SHARED_REPO_2} --upstreams repositoryName=pypi-store --profile ${AWS_PROFILE_1}


cat > readonly_repository_policy.json << EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "codeartifact:DescribePackageVersion",
                "codeartifact:DescribeRepository",
                "codeartifact:GetPackageVersionReadme",
                "codeartifact:GetRepositoryEndpoint",
                "codeartifact:ListPackages",
                "codeartifact:ListPackageVersions",
                "codeartifact:ListPackageVersionAssets",
                "codeartifact:ListPackageVersionDependencies",
                "codeartifact:ReadFromRepository"
            ],
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::${ACCOUNT_2_ID}:root"
            },
            "Resource": "*"
        }
    ]
}
EOF

aws codeartifact put-repository-permissions-policy --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} \
  --repository ${ACCOUNT_1_SHARED_REPO_2} --policy-document file://readonly_repository_policy.json --profile ${AWS_PROFILE_1}

rm readonly_repository_policy.json

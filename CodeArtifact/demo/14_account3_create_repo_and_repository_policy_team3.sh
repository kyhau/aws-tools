#!/bin/bash
set -e

source .env

AWS_PROFILE=${AWS_PROFILE_3}
REPO=${ACCOUNT_3_TEAM_3_REPO}

aws codeartifact create-repository --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} \
  --repository ${REPO} --description "Team repository" --profile ${AWS_PROFILE}


cat > policy.json << EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "ReadAccess",
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
            "Resource": "*",
            "Principal": {
                "AWS": [
                  "arn:aws:iam::${ACCOUNT_3_ID}:root"
                ]
            }
        }
    ]
}
EOF

aws codeartifact put-repository-permissions-policy --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} \
  --repository ${REPO} --policy-document file://policy.json --profile ${AWS_PROFILE}

rm policy.json

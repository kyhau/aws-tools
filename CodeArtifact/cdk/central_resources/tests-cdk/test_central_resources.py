from os.path import (
    dirname,
    join,
    realpath,
)

import pytest
import yaml
from aws_cdk import (
    App,
    Aspects,
    Environment,
)
from aws_cdk.assertions import (
    Template,
)
from cdk_nag import (
    AwsSolutionsChecks,
    HIPAASecurityChecks,
)
from lib.central_resources import (
    CodeArtifactCentralResources,
)

ENV_DIR = join(
    dirname(dirname(dirname(realpath(__file__)))),
    "environment",
)


@pytest.mark.parametrize(
    ("env"),
    [("dev"), ("prd")],
)
def test_synthesizes_properly(
    env,
):
    with open(
        join(
            ENV_DIR,
            f"{env}.yaml",
        ),
        "r",
    ) as stream:
        yaml_data = yaml.safe_load(stream)
        config = yaml_data if yaml_data is not None else {}

    app = App()

    _stack = CodeArtifactCentralResources(
        app,
        "TestCodeArtifactCentralResources",
        config=config,
        env=Environment(
            account=config["AWS_ACCOUNT"],
            region=config["AWS_REGION"],
        ),
        termination_protection=True,
    )

    # Add AWS Solutions and HIPAA Security checks
    Aspects.of(app).add(AwsSolutionsChecks(verbose=True))
    Aspects.of(app).add(HIPAASecurityChecks(verbose=True))

    # Prepare the stack for assertions.
    template = Template.from_stack(_stack)

    template.resource_count_is(
        "AWS::CodeArtifact::Domain",
        1,
    )

    ################################################################################
    # Check kms key

    # Assert it creates the function with the correct properties.
    template.has_resource_properties(
        "AWS::KMS::Alias",
        {
            "AliasName": f"alias/codeartifact-{config['DOMAIN_NAME']}",
        },
    )

    template.has_resource_properties(
        "AWS::KMS::Key",
        {
            "EnableKeyRotation": True,
            "KeyPolicy": {
                "Statement": [
                    {
                        "Action": "kms:*",
                        "Effect": "Allow",
                        "Principal": {
                            "AWS": {
                                "Fn::Join": [
                                    "",
                                    [
                                        "arn:",
                                        {"Ref": "AWS::Partition"},
                                        f":iam::{config['AWS_ACCOUNT']}:root",
                                    ],
                                ]
                            }
                        },
                        "Resource": "*",
                        "Sid": "EnableIAMUserPermissions",
                    },
                    {
                        "Action": [
                            "kms:Create*",
                            "kms:Describe*",
                            "kms:Enable*",
                            "kms:List*",
                            "kms:Put*",
                            "kms:Update*",
                            "kms:Revoke*",
                            "kms:Disable*",
                            "kms:Get*",
                            "kms:Delete*",
                            "kms:TagResource",
                            "kms:UntagResource",
                            "kms:ScheduleKeyDeletion",
                            "kms:CancelKeyDeletion",
                        ],
                        "Effect": "Allow",
                        "Principal": {"AWS": config["KEY_ADMIN_ARNS"]},
                        "Resource": "*",
                        "Sid": "AllowAccessForKeyAdministrators",
                    },
                ]
            },
        },
    )

    ################################################################################
    # Check domain

    # Assert it creates the function with the correct properties.
    template.has_resource_properties(
        "AWS::CodeArtifact::Domain",
        {
            "DomainName": config["DOMAIN_NAME"],
            "EncryptionKey": {
                "Fn::Join": [
                    "",
                    [
                        "arn:",
                        {"Ref": "AWS::Partition"},
                        f":kms:ap-southeast-2:{config['AWS_ACCOUNT']}:alias/codeartifact-{config['DOMAIN_NAME']}",
                    ],
                ]
            },
            "PermissionsPolicyDocument": {
                "Statement": [
                    {
                        "Condition": {
                            "StringEquals": {"aws:PrincipalOrgId": [config["AWS_ORG_ID"]]}
                        },
                        "Effect": "Allow",
                    }
                ]
            },
        },
    )

    # Check number of repos - 10 external and 1 internal
    template.resource_count_is(
        "AWS::CodeArtifact::Repository",
        11,
    )

    ################################################################################
    # Check external connection repos

    template.has_resource_properties(
        "AWS::CodeArtifact::Repository",
        {
            "DomainName": config["DOMAIN_NAME"],
            "DomainOwner": config["AWS_ACCOUNT"],
            "ExternalConnections": ["public:crates-io"],
            "PermissionsPolicyDocument": {
                "Statement": [
                    {
                        "Condition": {
                            "StringEquals": {"aws:PrincipalOrgId": [config["AWS_ORG_ID"]]}
                        },
                        "Effect": "Allow",
                    }
                ]
            },
            "RepositoryName": "external-crates-io",
        },
    )

    template.has_resource_properties(
        "AWS::CodeArtifact::Repository",
        {
            "DomainName": config["DOMAIN_NAME"],
            "DomainOwner": config["AWS_ACCOUNT"],
            "ExternalConnections": ["public:maven-central"],
            "PermissionsPolicyDocument": {
                "Statement": [
                    {
                        "Condition": {
                            "StringEquals": {"aws:PrincipalOrgId": [config["AWS_ORG_ID"]]}
                        },
                        "Effect": "Allow",
                    }
                ]
            },
            "RepositoryName": "external-maven-central",
        },
    )

    template.has_resource_properties(
        "AWS::CodeArtifact::Repository",
        {
            "DomainName": config["DOMAIN_NAME"],
            "DomainOwner": config["AWS_ACCOUNT"],
            "ExternalConnections": ["public:maven-clojars"],
            "PermissionsPolicyDocument": {
                "Statement": [
                    {
                        "Condition": {
                            "StringEquals": {"aws:PrincipalOrgId": [config["AWS_ORG_ID"]]}
                        },
                        "Effect": "Allow",
                    }
                ]
            },
            "RepositoryName": "external-maven-clojars",
        },
    )
    template.has_resource_properties(
        "AWS::CodeArtifact::Repository",
        {
            "DomainName": config["DOMAIN_NAME"],
            "DomainOwner": config["AWS_ACCOUNT"],
            "ExternalConnections": ["public:maven-commonsware"],
            "PermissionsPolicyDocument": {
                "Statement": [
                    {
                        "Condition": {
                            "StringEquals": {"aws:PrincipalOrgId": [config["AWS_ORG_ID"]]}
                        },
                        "Effect": "Allow",
                    }
                ]
            },
            "RepositoryName": "external-maven-commonsware",
        },
    )
    template.has_resource_properties(
        "AWS::CodeArtifact::Repository",
        {
            "DomainName": config["DOMAIN_NAME"],
            "DomainOwner": config["AWS_ACCOUNT"],
            "ExternalConnections": ["public:maven-googleandroid"],
            "PermissionsPolicyDocument": {
                "Statement": [
                    {
                        "Condition": {
                            "StringEquals": {"aws:PrincipalOrgId": [config["AWS_ORG_ID"]]}
                        },
                        "Effect": "Allow",
                    }
                ]
            },
            "RepositoryName": "external-maven-googleandroid",
        },
    )
    template.has_resource_properties(
        "AWS::CodeArtifact::Repository",
        {
            "DomainName": config["DOMAIN_NAME"],
            "DomainOwner": config["AWS_ACCOUNT"],
            "ExternalConnections": ["public:maven-gradleplugins"],
            "PermissionsPolicyDocument": {
                "Statement": [
                    {
                        "Condition": {
                            "StringEquals": {"aws:PrincipalOrgId": [config["AWS_ORG_ID"]]}
                        },
                        "Effect": "Allow",
                    }
                ]
            },
            "RepositoryName": "external-maven-gradleplugins",
        },
    )
    template.has_resource_properties(
        "AWS::CodeArtifact::Repository",
        {
            "DomainName": config["DOMAIN_NAME"],
            "DomainOwner": config["AWS_ACCOUNT"],
            "ExternalConnections": ["public:npmjs"],
            "PermissionsPolicyDocument": {
                "Statement": [
                    {
                        "Condition": {
                            "StringEquals": {"aws:PrincipalOrgId": [config["AWS_ORG_ID"]]}
                        },
                        "Effect": "Allow",
                    }
                ]
            },
            "RepositoryName": "external-npmjs",
        },
    )
    template.has_resource_properties(
        "AWS::CodeArtifact::Repository",
        {
            "DomainName": config["DOMAIN_NAME"],
            "DomainOwner": config["AWS_ACCOUNT"],
            "ExternalConnections": ["public:nuget-org"],
            "PermissionsPolicyDocument": {
                "Statement": [
                    {
                        "Condition": {
                            "StringEquals": {"aws:PrincipalOrgId": [config["AWS_ORG_ID"]]}
                        },
                        "Effect": "Allow",
                    }
                ]
            },
            "RepositoryName": "external-nuget-org",
        },
    )
    template.has_resource_properties(
        "AWS::CodeArtifact::Repository",
        {
            "DomainName": config["DOMAIN_NAME"],
            "DomainOwner": config["AWS_ACCOUNT"],
            "ExternalConnections": ["public:pypi"],
            "PermissionsPolicyDocument": {
                "Statement": [
                    {
                        "Condition": {
                            "StringEquals": {"aws:PrincipalOrgId": [config["AWS_ORG_ID"]]}
                        },
                        "Effect": "Allow",
                    }
                ]
            },
            "RepositoryName": "external-pypi",
        },
    )
    template.has_resource_properties(
        "AWS::CodeArtifact::Repository",
        {
            "DomainName": config["DOMAIN_NAME"],
            "DomainOwner": config["AWS_ACCOUNT"],
            "ExternalConnections": ["public:ruby-gems-org"],
            "PermissionsPolicyDocument": {
                "Statement": [
                    {
                        "Condition": {
                            "StringEquals": {"aws:PrincipalOrgId": [config["AWS_ORG_ID"]]}
                        },
                        "Effect": "Allow",
                    }
                ]
            },
            "RepositoryName": "external-ruby-gems-org",
        },
    )

    ################################################################################
    # Check internal shared repo

    template.has_resource_properties(
        "AWS::CodeArtifact::Repository",
        {
            "DomainName": config["DOMAIN_NAME"],
            "DomainOwner": config["AWS_ACCOUNT"],
            "RepositoryName": config["INTERNAL_SHARED_REPO"],
            "PermissionsPolicyDocument": {
                "Statement": [
                    {
                        "Condition": {
                            "StringEquals": {"aws:PrincipalOrgId": [config["AWS_ORG_ID"]]}
                        },
                        "Effect": "Allow",
                        "Sid": "ReadAccess",
                    },
                    {
                        "Condition": {
                            "ArnLike": {
                                "aws:PrincipalArn": [
                                    "arn:aws:iam::459220104973:role/*/github/GHRunnerExecRole*",
                                    "arn:aws:iam::529177531254:role/*/github/GHRunnerExecRole*",
                                ]
                            }
                        },
                        "Effect": "Allow",
                        "Principal": {
                            "AWS": [
                                "arn:aws:iam::459220104973:root",
                                "arn:aws:iam::529177531254:root",
                            ]
                        },
                        "Sid": "WriteAccess",
                    },
                ]
            },
            "Upstreams": [
                "external-crates-io",
                "external-maven-central",
                "external-maven-clojars",
                "external-maven-commonsware",
                "external-maven-googleandroid",
                "external-maven-gradleplugins",
                "external-npmjs",
                "external-nuget-org",
                "external-pypi",
                "external-ruby-gems-org",
            ],
        },
    )

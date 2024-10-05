#!/usr/bin/env python3
from os.path import dirname, join, realpath

import yaml
from aws_cdk import App, CfnOutput, CliCredentialsStackSynthesizer, Environment, Stack, Tags
from aws_cdk import aws_iam as iam
from aws_cdk.aws_codeartifact import CfnRepository
from constructs import Construct

ENV_DIR = join(dirname(realpath(__file__)), "environment")


class CodeArtifactRepoStack(Stack):
    def __init__(self, scope: Construct, id: str, config: dict, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create CodeArtifact repository
        repo = CfnRepository(
            self,
            "CodeArtifactRepo",
            description="Default repository for sharing within the AWS Organization with upstreams internal-shared and external connections.",
            domain_name=config["DOMAIN_NAME"],
            domain_owner=config["DOMAIN_OWNER"],
            repository_name=config["REPO_NAME"],
            upstreams=config["UPSTREAMS"],
            permissions_policy_document=iam.PolicyDocument(
                statements=[
                    iam.PolicyStatement(
                        sid="ReadOnlyRepositoryAccess",
                        effect=iam.Effect.ALLOW,
                        actions=[
                            "codeartifact:DescribePackageVersion",
                            "codeartifact:DescribeRepository",
                            "codeartifact:GetPackageVersionReadme",
                            "codeartifact:GetRepositoryEndpoint",
                            "codeartifact:ListPackages",
                            "codeartifact:ListPackageVersions",
                            "codeartifact:ListPackageVersionAssets",
                            "codeartifact:ListPackageVersionDependencies",
                            "codeartifact:ListTagsForResource",
                            "codeartifact:ReadFromRepository",
                        ],
                        resources=["*"],
                        principals=[iam.AnyPrincipal()],
                        conditions={"StringEquals": {"aws:PrincipalOrgId": [config["AWS_ORG_ID"]]}},
                    ),
                    iam.PolicyStatement(
                        sid="WriteRepositoryAccess",
                        effect=iam.Effect.ALLOW,
                        actions=[
                            "codeartifact:CopyPackageVersions",
                            "codeartifact:DeletePackage",
                            "codeartifact:DeletePackageVersions",
                            "codeartifact:PublishPackageVersion",
                            "codeartifact:PutPackageMetadata",
                        ],
                        resources=["*"],
                        principals=[iam.AnyPrincipal()],
                        conditions={
                            "ArnLike": {"aws:PrincipalArn": config["REPO_WRITE_ACCESS_ARNS_LIKE"]}
                        },
                    ),
                    iam.PolicyStatement(
                        sid="FullRepositoryAccess",
                        effect=iam.Effect.ALLOW,
                        actions=[
                            "codeartifact:AssociateExternalConnection",
                            "codeartifact:CopyPackageVersions",
                            "codeartifact:DeletePackage",
                            "codeartifact:DeletePackageVersions",
                            "codeartifact:DeleteRepository",
                            "codeartifact:DeleteRepositoryPermissionsPolicy",
                            "codeartifact:DescribePackageVersion",
                            "codeartifact:DescribeRepository",
                            "codeartifact:DisassociateExternalConnection",
                            "codeartifact:DisposePackageVersions",
                            "codeartifact:GetPackageVersionReadme",
                            "codeartifact:GetRepositoryEndpoint",
                            "codeartifact:ListPackageVersionAssets",
                            "codeartifact:ListPackageVersionDependencies",
                            "codeartifact:ListPackageVersions",
                            "codeartifact:ListPackages",
                            "codeartifact:PublishPackageVersion",
                            "codeartifact:PutPackageMetadata",
                            "codeartifact:PutRepositoryPermissionsPolicy",
                            "codeartifact:ReadFromRepository",
                            "codeartifact:TagResource",
                            "codeartifact:UpdatePackageVersionsStatus",
                            "codeartifact:UpdateRepository",
                            "codeartifact:UntagResource",
                        ],
                        resources=["*"],
                        principals=[iam.AnyPrincipal()],
                        conditions={
                            "ArnLike": {"aws:PrincipalArn": config["REPO_FULL_ACCESS_ARNS_LIKE"]}
                        },
                    ),
                ]
            ),
        )
        CfnOutput(self, "CodeArtifactRepoArn", value=repo.attr_arn)
        CfnOutput(self, "CodeArtifactRepoDomainName", value=repo.attr_domain_name)
        CfnOutput(self, "CodeArtifactRepoDomainOwner", value=repo.attr_domain_owner)
        CfnOutput(self, "CodeArtifactRepoName", value=repo.attr_name)


def main():
    app = App()

    ENV_NAME = app.node.try_get_context("env") or "dev"

    with open(join(ENV_DIR, f"{ENV_NAME}.yml"), "r") as stream:
        yaml_data = yaml.safe_load(stream)
        config = yaml_data if yaml_data is not None else {}

    stack = CodeArtifactRepoStack(
        scope=app,
        id="CodeArtifactRepoStack",
        config=config,
        env=Environment(
            account=config["AWS_ACCOUNT"],
            region=config["AWS_REGION"],
        ),
        synthesizer=CliCredentialsStackSynthesizer(),
        termination_protection=(ENV_NAME == "prd"),
    )

    for key, value in config["TAGS"].items():
        Tags.of(stack).add(key, value)

    app.synth()


if __name__ == "__main__":
    main()

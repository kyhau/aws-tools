from aws_cdk import CfnOutput, Stack, aws_iam, aws_kms
from aws_cdk.aws_codeartifact import CfnDomain, CfnRepository
from constructs import Construct
from lib.kms import create_kms_key_and_alias


class CodeArtifactCentralResources(Stack):
    def __init__(self, scope: Construct, id: str, config: dict, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        key_admin_arns = [
            aws_iam.Role.from_role_arn(
                self,
                arn_str.split("/")[-1],
                arn_str,
            )
            for arn_str in config["KEY_ADMIN_ARNS"]
        ]

        key_alias = create_kms_key_and_alias(
            self,
            "CodeArtifactKey",
            key_alias=f"alias/codeartifact-{config['DOMAIN_NAME']}",
            key_admin_arns=key_admin_arns,
        )

        # Create CodeArtifact domain
        domain = self.create_domain_with_domain_policy(
            config["DOMAIN_NAME"],
            config["AWS_ORG_ID"],
            key_alias,
        )
        domain.add_dependency(key_alias.node.default_child)  # casting L1/L2 construct

        read_only_statement = self.create_read_policy_statament(config["AWS_ORG_ID"])

        # Create external connection repos
        external_conn_repos = [
            self.create_external_connection_repo(
                domain,
                external_conn,
                read_only_statement,
            )
            for external_conn in config["EXTERNAL_CONNECTIONS"]
        ]

        write_statement = self.create_write_policy_statament(config["WRITE_ROLE_ARNS_LIKE"])

        # Create internal shared repos with upstreams as the external connection repos
        internal_shared_repo = self.create_internal_shared_repo(
            domain,
            config["INTERNAL_SHARED_REPO"],
            external_conn_repos,
            read_only_statement,
            write_statement,
        )

        CfnOutput(self, "CodeArtifactDomainName", value=domain.domain_name)
        CfnOutput(self, "CodeArtifactDomainOwner", value=self.account)
        CfnOutput(self, "InternalSharedRepoName", value=internal_shared_repo.repository_name)

    def create_domain_with_domain_policy(
        self,
        domain_name: str,
        org_id: str,
        key_alias: aws_kms.Alias,
    ) -> CfnDomain:
        return CfnDomain(
            self,
            "CodeArtifactDomain",
            domain_name=domain_name,
            encryption_key=key_alias.key_arn,
            permissions_policy_document=aws_iam.PolicyDocument(
                statements=[
                    aws_iam.PolicyStatement(
                        actions=[
                            "codeartifact:CreateRepository",
                            "codeartifact:DescribeDomain",
                            "codeartifact:GetAuthorizationToken",
                            "codeartifact:GetDomainPermissionsPolicy",
                            "codeartifact:ListRepositoriesInDomain",
                        ],
                        conditions={"StringEquals": {"aws:PrincipalOrgId": [org_id]}},
                        effect=aws_iam.Effect.ALLOW,
                        principals=[aws_iam.AnyPrincipal()],
                        resources=["*"],
                        sid="DomainPolicyForOrganization",
                    ),
                ]
            ),
        )

    def create_external_connection_repo(
        self,
        domain: CfnDomain,
        external_conn: str,
        read_only_statement: aws_iam.PolicyStatement,
    ) -> CfnRepository:
        repo = CfnRepository(
            self,
            f"ExternalConnection{external_conn.capitalize()}",
            description=f"External connection {external_conn}",
            domain_name=domain.domain_name,
            domain_owner=self.account,
            external_connections=[f"public:{external_conn}"],
            permissions_policy_document=aws_iam.PolicyDocument(statements=[read_only_statement]),
            repository_name=f"external-{external_conn}",
        )
        repo.add_dependency(domain)
        return repo

    def create_internal_shared_repo(
        self,
        domain: CfnDomain,
        internal_shared_repo: str,
        external_conn_repos: list,
        read_only_statement: aws_iam.PolicyStatement,
        write_statement: aws_iam.PolicyStatement,
    ) -> CfnRepository:
        external_conn_repo_names = [repo.repository_name for repo in external_conn_repos]

        repo = CfnRepository(
            self,
            "InternalSharedRepo",
            description="Internal shared",
            domain_name=domain.domain_name,
            domain_owner=self.account,
            permissions_policy_document=aws_iam.PolicyDocument(
                statements=[
                    read_only_statement,
                    write_statement,
                ]
            ),
            repository_name=internal_shared_repo,
            upstreams=external_conn_repo_names,
        )

        repo.add_dependency(domain)
        for external_conn_repo in external_conn_repos:
            repo.add_dependency(external_conn_repo)

        return repo

    def create_read_policy_statament(self, org_id: str):
        return aws_iam.PolicyStatement(
            actions=[
                "codeartifact:AssociateWithDownstreamRepository",
                "codeartifact:DescribePackageVersion",
                "codeartifact:DescribeRepository",
                "codeartifact:GetPackageVersionAsset",
                "codeartifact:GetPackageVersionReadme",
                "codeartifact:GetRepositoryEndpoint",
                "codeartifact:GetRepositoryPermissionsPolicy",
                "codeartifact:ListPackages",
                "codeartifact:ListPackageVersions",
                "codeartifact:ListPackageVersionAssets",
                "codeartifact:ListPackageVersionDependencies",
                "codeartifact:ListTagsForResource",
                "codeartifact:ReadFromRepository",
            ],
            conditions={"StringEquals": {"aws:PrincipalOrgId": [org_id]}},
            effect=aws_iam.Effect.ALLOW,
            principals=[aws_iam.AnyPrincipal()],
            resources=["*"],
            sid="ReadAccess",
        )

    def create_write_policy_statament(
        self,
        write_role_arn_like_list: list,
    ):
        """
        Note: WriteAccess is on request - add to `conditions` and `principal` below
        """

        account_ids = [arn.split(":")[4] for arn in write_role_arn_like_list]
        root_principals = [
            aws_iam.ArnPrincipal(f"arn:aws:iam::{account_id}:root") for account_id in account_ids
        ]

        return aws_iam.PolicyStatement(
            actions=[
                "codeartifact:CopyPackageVersions",
                "codeartifact:DeletePackage",
                "codeartifact:DeletePackageVersions",
                "codeartifact:PublishPackageVersion",
                "codeartifact:PutPackageMetadata",
            ],
            conditions={"ArnLike": {"aws:PrincipalArn": write_role_arn_like_list}},
            effect=aws_iam.Effect.ALLOW,
            principals=root_principals,
            resources=["*"],
            sid="WriteAccess",
        )

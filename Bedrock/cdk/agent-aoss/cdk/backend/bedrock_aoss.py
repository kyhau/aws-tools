import json
import platform
from pathlib import Path

from aws_cdk import CfnOutput, CustomResource, Duration, RemovalPolicy
from aws_cdk import aws_bedrock as bedrock_
from aws_cdk import aws_ec2 as ec2_
from aws_cdk import aws_ecr_assets
from aws_cdk import aws_iam as iam_
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_opensearchserverless as aoss_
from aws_cdk import aws_s3 as s3_
from aws_cdk import aws_s3_notifications as s3n_
from aws_cdk import aws_ssm as ssm_
from aws_cdk import custom_resources
from aws_cdk.aws_logs import RetentionDays
from constructs import Construct

LAMBDA_COLLECTIONS = (Path(__file__).parents[2] / "app" / "lambda" / "collections").as_posix()
LAMBDA_KB_SYNC = (Path(__file__).parents[2] / "app" / "lambda" / "kb_sync").as_posix()


def get_aoss_vpce_id(scope: Construct) -> str:
    return ssm_.StringParameter.value_for_string_parameter(
        scope, "/account/vpce-aoss/aossVpcEndpointId"
    )


def get_aoss_vpce_sg_immutable(scope: Construct, id: str) -> ec2_.ISecurityGroup:
    aoss_vpce_sg_id = ssm_.StringParameter.value_for_string_parameter(
        scope, "/account/vpce-aoss/aossVpcEndpointSGId"
    )
    return ec2_.SecurityGroup.from_security_group_id(scope, id, aoss_vpce_sg_id, mutable=False)


def get_vpc(scope: Construct, id: str = "myVpc") -> ec2_.IVpc:
    vpc_id = ssm_.StringParameter.value_for_string_parameter(
        scope, "/account/vpc/vpcId",
    )
    return ec2_.Vpc.from_lookup(scope, id, is_default=False, vpc_id=vpc_id)


def get_subnets(scope: Construct, id: str = "mySubnets") -> ec2_.SubnetSelection:
    app_subnet_ids_params = [f"/account/vpc/appSubnetId{i}" for i in range(3)]
    return ec2_.SubnetSelection(
        subnets=[
            ec2_.Subnet.from_subnet_id(
                scope,
                f"{id}AppSubnet{i}",
                ssm_.StringParameter.value_from_lookup(scope, subnet_id_param),
            )
            for i, subnet_id_param in enumerate(app_subnet_ids_params)
        ]
    )


class AgentWithAOSSKB(Construct):
    """
    Create S3 Bucket, Bedrock Agent, Knowledge Base, and Amazon OpenSearch Service
    """

    def __init__(
        self,
        scope: Construct,
        id: str,
        agent_instructions: str = "You are a comedian tasked with telling bad jokes regardless of user input",
        agent_model_id: str = "anthropic.claude-3-5-sonnet-20241022-v2:0",
        agent_alias_name: str = "v1",
        embeddings_model_id: str = "cohere.embed-english-v3",
        embeddings_vector_size: int = 1024,
        lambda_architecture: lambda_.Architecture | None = None,
        lambda_platform: aws_ecr_assets.Platform | None = None,
        log_retention_in_days: RetentionDays | None = RetentionDays.ONE_DAY,
    ):
        super().__init__(scope, id)
        self.id = id
        self.log_retention_in_days = log_retention_in_days

        # Default to current platform, useful since we'll compile the docker images
        if lambda_architecture is None or lambda_architecture is None:
            match platform.machine():
                case "amd64":
                    lambda_architecture = lambda_.Architecture.ARM_64
                    lambda_platform = aws_ecr_assets.Platform.LINUX_ARM64
                case _:
                    lambda_architecture = lambda_.Architecture.X86_64
                    lambda_platform = aws_ecr_assets.Platform.LINUX_AMD64

        # Create S3 bucket that will be used for our storage needs
        bucket = self.create_bucket_storage()

        # Create OpenSearch Serverless collection
        collection = self.create_opensearch_serverless_collection()

        # Lambda CustomResource for creating the index in the Collection
        index_creator, index_lambda_role = self.create_index_collector_function_and_role(
            lambda_architecture,
            lambda_platform,
            collection,
            embeddings_vector_size,
        )

        # Create the knowledge base in the collection using the provided FM model and role
        knowledge_base, kb_role = self.create_knowledge_base(
            embeddings_model_id, index_creator, collection
        )

        bucket.grant_read(kb_role)

        # Creat OpenSearch data access policy
        self.create_opensearch_data_access_policy(collection, kb_role, index_lambda_role)

        # Create the data source
        data_source = self.create_data_source(knowledge_base=knowledge_base, bucket=bucket)

        # This lambda will take care of issuing an update command on the Knowledge Base if files
        # are added to/removed from the S3 bucket
        self.create_kb_sync_lambda(
            lambda_architecture,
            lambda_platform,
            bucket,
            data_source,
            knowledge_base,
        )

        # Finally, create the Bedrock Agent for this knowledge base
        agent, agent_alias = self.create_bedrock_agent_for_knowledge_base(
            agent_model_id, agent_alias_name, agent_instructions, knowledge_base
        )

        # Make stack attributes available
        self.agent = agent
        self.agent_alias = agent_alias
        self.bucket = bucket

        # Declare the stack outputs
        CfnOutput(
            scope=self,
            id="AgentName",
            value=agent.agent_name,
            description="The name of the Bedrock Agent",
        )
        CfnOutput(
            scope=self,
            id="CollectionId",
            value=collection.logical_id,
            description="The ID of the vector database collection",
        )
        CfnOutput(
            scope=self,
            id="KnowledgeBaseBucket",
            value=bucket.bucket_name,
            description="The data source S3 bucket of the knowledge base",
        )
        CfnOutput(
            scope=self,
            id="KnowledgeBaseId",
            value=knowledge_base.attr_knowledge_base_id,
            description="Knowledge base ID",
        )

    def create_bucket_storage(self) -> s3_.Bucket:
        """S3 bucket that will be used for our storage needs"""
        return s3_.Bucket(
            scope=self,
            id="KBDocsBucket",
            versioned=False,
            encryption=s3_.BucketEncryption.S3_MANAGED,
            event_bridge_enabled=True,
            removal_policy=RemovalPolicy.DESTROY,
            enforce_ssl=True,
            auto_delete_objects=True,
        )

    def create_opensearch_serverless_collection(self) -> aoss_.CfnCollection:
        collection = aoss_.CfnCollection(
            scope=self,
            id="AgentCollection",
            name=f"{self.id.lower()}-collection",
            description=f"{self.id} Embeddings Store",
            standby_replicas="DISABLED",
            type="VECTORSEARCH",
        )
        encryption_policy_document = json.dumps(
            {
                "Rules": [
                    {"ResourceType": "collection", "Resource": [f"collection/{collection.name}"]}
                ],
                "AWSOwnedKey": True,
            },
            separators=(",", ":"),
        )
        encryption_policy = aoss_.CfnSecurityPolicy(
            scope=self,
            id="CollectionEncryptionPolicy",
            name=f"{self.id.lower()}-colln-encryptn",
            type="encryption",
            policy=encryption_policy_document,
        )
        collection.add_dependency(encryption_policy)

        aoss_vpce_id = get_aoss_vpce_id(self)

        network_policy_document = json.dumps(
            [
                {
                    "Rules": [
                        {
                            "Resource": [f"collection/{collection.name}"],
                            "ResourceType": "collection",
                        },
                        {
                            "Resource": [f"collection/{collection.name}"],
                            "ResourceType": "dashboard",
                        },
                    ],
                    # See also https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-network.html#serverless-network-cli
                    "AllowFromPublic": False,
                    "SourceServices": ["bedrock.amazonaws.com"],
                    "SourceVPCEs": [aoss_vpce_id],
                }
            ],
            separators=(",", ":"),
        )
        network_policy = aoss_.CfnSecurityPolicy(
            scope=self,
            id="CollectionNetworkPolicy",
            name=f"{self.id.lower()}-colln-network",
            type="network",
            policy=network_policy_document,
        )
        collection.add_dependency(network_policy)
        return collection

    def create_opensearch_data_access_policy(
        self, collection: aoss_.CfnCollection, kb_role: iam_.Role, index_lambda_role: iam_.Role
    ) -> aoss_.CfnAccessPolicy:
        policy = json.dumps(
            [
                {
                    "Description": "Agent data policy",
                    "Principal": [
                        index_lambda_role.role_arn,
                        kb_role.role_arn,
                    ],
                    "Rules": [
                        {
                            "Resource": [f"collection/{collection.name}"],
                            "Permission": [
                                "aoss:CreateCollectionItems",
                                "aoss:DeleteCollectionItems",
                                "aoss:UpdateCollectionItems",
                                "aoss:DescribeCollectionItems",
                            ],
                            "ResourceType": "collection",
                        },
                        {
                            "Resource": [f"index/{collection.name}/*"],
                            "Permission": [
                                "aoss:CreateIndex",
                                "aoss:DeleteIndex",
                                "aoss:UpdateIndex",
                                "aoss:DescribeIndex",
                                "aoss:ReadDocument",
                                "aoss:WriteDocument",
                            ],
                            "ResourceType": "index",
                        },
                    ],
                }
            ],
            separators=(",", ":"),
        )
        data_access_policy = aoss_.CfnAccessPolicy(
            scope=self,
            id="DataAccessPolicy",
            name=f"{self.id.lower()}-data-access",
            type="data",
            policy=policy,
        )
        collection.add_dependency(data_access_policy)
        return data_access_policy

    def create_index_collector_function_and_role(
        self,
        lambda_architecture: lambda_.Architecture,
        lambda_platform: aws_ecr_assets.Platform,
        collection: aoss_.CfnCollection,
        embeddings_vector_size: int,
    ) -> tuple[CustomResource, iam_.Role]:
        function_name = "CollectionIndexCreator"

        index_lambda_role = iam_.Role(
            scope=self,
            id=f"{function_name}-ExecutionRole",
            assumed_by=iam_.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam_.ManagedPolicy.from_aws_managed_policy_name(name) for name in [
                    "service-role/AWSLambdaBasicExecutionRole",
                    "service-role/AWSLambdaVPCAccessExecutionRole",
                    "AWSXrayWriteOnlyAccess",
                    "CloudWatchLambdaApplicationSignalsExecutionRolePolicy",
                ]
            ],
            role_name=f"{self.id}-{function_name}-ExecutionRole",
        )

        # Give permissions to the Lambda Role to execute the AWS API operations
        index_lambda_role.add_to_policy(
            iam_.PolicyStatement(
                sid="IndexCreation",
                actions=["aoss:APIAccessAll"],
                effect=iam_.Effect.ALLOW,
                resources=[collection.attr_arn],
            )
        )

        # TODO uncomment the following
        # acc_vpc = get_vpc(self, id="accVpc")
        # acc_subnets = get_subnets(self, id="acc")
        # aoss_vpce_sg = get_aoss_vpce_sg_immutable(self)

        # Lambda CustomResource for creating the index in the Collection
        image = lambda_.DockerImageCode.from_image_asset(
            LAMBDA_COLLECTIONS, platform=lambda_platform
        )
        cust_res_lambda = lambda_.DockerImageFunction(
            scope=self,
            id=function_name,
            architecture=lambda_architecture,
            code=image,
            environment={
                "AWS_LAMBDA_EXEC_WRAPPER": "/opt/otel-instrument",  # for OpenTelemetry
            },
            function_name=f"{self.id}-{function_name}",
            role=index_lambda_role,
            log_retention=self.log_retention_in_days,
            timeout=Duration.seconds(60),
            tracing=lambda_.Tracing.ACTIVE,
            # TODO uncomment the following
            # vpc=acc_vpc,
            # vpc_subnets=acc_subnets,
            # security_groups=[aoss_vpce_sg],
        )

        res_provider = custom_resources.Provider(
            scope=self,
            id="CustomResourceIndexCreator",
            on_event_handler=cust_res_lambda,
        )

        index_creator = CustomResource(
            scope=self,
            id="CustomCollectionIndexCreator",
            service_token=res_provider.service_token,
            properties={
                "collection": collection.name,
                "endpoint": collection.attr_collection_endpoint,
                "vector_index_name": "bedrock-knowledge-base-default-index",
                "vector_size": embeddings_vector_size,  # Depends on embeddings model
                "metadata_field": "AMAZON_BEDROCK_METADATA",
                "text_field": "AMAZON_BEDROCK_TEXT_CHUNK",
                "vector_field": "bedrock-knowledge-base-default-vector",
            },
        )
        index_creator.node.add_dependency(collection)
        return index_creator, index_lambda_role

    def create_knowledge_base(
        self,
        embeddings_model_id: str,
        index_creator: CustomResource,
        collection: aoss_.CfnCollection,
    ) -> tuple[bedrock_.CfnKnowledgeBase, iam_.Role]:
        """
        Create the knowledge base in the collection using the provided FM model and role
        """
        # Bedrock Fundation Model
        model_arn = bedrock_.FoundationModel.from_foundation_model_id(
            scope=self,
            _id="EmbeddingsModel",
            foundation_model_id=bedrock_.FoundationModelIdentifier(embeddings_model_id),
        ).model_arn

        # Role that will be used by the KB
        kb_role = iam_.Role(
            scope=self,
            id="AgentKBRole",
            assumed_by=iam_.ServicePrincipal("bedrock.amazonaws.com"),
            role_name=f"{self.id}-AgentKBRole",
        )
        kb_role.add_to_policy(
            iam_.PolicyStatement(
                sid="OpenSearchServerlessAPIAccessAll",
                actions=["aoss:APIAccessAll"],
                effect=iam_.Effect.ALLOW,
                resources=[collection.attr_arn],
            )
        )
        kb_role.add_to_policy(
            iam_.PolicyStatement(
                sid="BedrockInvokeModel",
                actions=["bedrock:InvokeModel"],
                effect=iam_.Effect.ALLOW,
                resources=[model_arn],
            )
        )

        knowledge_base = bedrock_.CfnKnowledgeBase(
            scope=self,
            id="AgentKB",
            name=f"{self.id}-KB",
            role_arn=kb_role.role_arn,
            knowledge_base_configuration={
                "type": "VECTOR",
                "vectorKnowledgeBaseConfiguration": {"embeddingModelArn": model_arn},
            },
            storage_configuration={
                "type": "OPENSEARCH_SERVERLESS",
                "opensearchServerlessConfiguration": {
                    "collectionArn": collection.attr_arn,
                    "vectorIndexName": "bedrock-knowledge-base-default-index",
                    "fieldMapping": {
                        "metadataField": "AMAZON_BEDROCK_METADATA",
                        "textField": "AMAZON_BEDROCK_TEXT_CHUNK",
                        "vectorField": "bedrock-knowledge-base-default-vector",
                    },
                },
            },
        )
        knowledge_base.node.add_dependency(index_creator)
        return knowledge_base, kb_role

    def create_data_source(
        self, knowledge_base: bedrock_.CfnKnowledgeBase, bucket: s3_.Bucket
    ) -> bedrock_.CfnDataSource:
        return bedrock_.CfnDataSource(
            scope=self,
            id="KBDataSource",
            name=f"{self.id}-KBDataSource",
            knowledge_base_id=knowledge_base.attr_knowledge_base_id,
            data_source_configuration={
                "s3Configuration": {"bucketArn": bucket.bucket_arn},
                "type": "S3",
            },
            # The properties below are optional
            data_deletion_policy="RETAIN",
            description=f"{self.id}-KBDataSource",
            # TODO Define the chunking strategy
            # https://docs.aws.amazon.com/bedrock/latest/userguide/kb-chunking-parsing.html
        )

    def create_kb_sync_lambda(
        self,
        lambda_architecture: lambda_.Architecture,
        lambda_platform: aws_ecr_assets.Platform,
        bucket: s3_.Bucket,
        data_source: bedrock_.CfnDataSource,
        knowledge_base: bedrock_.CfnKnowledgeBase,
    ) -> tuple[lambda_.DockerImageFunction, iam_.Role]:
        """
        This lambda will take care of issuing an update command on the Knowledge Base if files
        are added to/removed from the S3 bucket
        """
        function_name = "KBSync"

        kb_lambda_role = iam_.Role(
            scope=self,
            id=f"{function_name}-ExecutionRole",
            assumed_by=iam_.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam_.ManagedPolicy.from_aws_managed_policy_name(name) for name in [
                    "service-role/AWSLambdaBasicExecutionRole",
                    "AWSXrayWriteOnlyAccess",
                    "CloudWatchLambdaApplicationSignalsExecutionRolePolicy",
                ]
            ],
            role_name=f"{self.id}-{function_name}-ExecutionRole",
        )

        kb_sync_lambda = lambda_.DockerImageFunction(
            scope=self,
            id=function_name,
            architecture=lambda_architecture,
            code=lambda_.DockerImageCode.from_image_asset(
                directory=LAMBDA_KB_SYNC, platform=lambda_platform
            ),
            environment={
                "KNOWLEDGE_BASE_ID": knowledge_base.attr_knowledge_base_id,
                "DATA_SOURCE_ID": data_source.attr_data_source_id,
                "AWS_LAMBDA_EXEC_WRAPPER": "/opt/otel-instrument",  # for OpenTelemetry
            },
            function_name=f"{self.id}-{function_name}",
            role=kb_lambda_role,
            log_retention=self.log_retention_in_days,
            timeout=Duration.minutes(15),
            tracing=lambda_.Tracing.ACTIVE,
        )

        kb_lambda_role.add_to_policy(
            iam_.PolicyStatement(
                sid="SyncKB",
                actions=["bedrock:StartIngestionJob"],
                effect=iam_.Effect.ALLOW,
                resources=[knowledge_base.attr_knowledge_base_arn],
            )
        )

        # Create the EventBridge rule so that the lambda is started when a
        # file is added to/removed from the S3 bucket
        bucket.add_event_notification(
            s3_.EventType.OBJECT_CREATED, s3n_.LambdaDestination(kb_sync_lambda)
        )
        bucket.add_event_notification(
            s3_.EventType.OBJECT_REMOVED, s3n_.LambdaDestination(kb_sync_lambda)
        )

        return kb_sync_lambda, kb_lambda_role

    def create_bedrock_agent_for_knowledge_base(
        self,
        agent_model_id: str,
        agent_alias_name: str,
        agent_instructions: str,
        knowledge_base: bedrock_.CfnKnowledgeBase,
    ) -> tuple[bedrock_.CfnAgent, bedrock_.CfnAgentAlias]:
        """
        Create the Bedrock Agent for this knowledge base
        """
        agent_model_arn = bedrock_.FoundationModel.from_foundation_model_id(
            scope=self,
            _id="AgentModel",
            foundation_model_id=bedrock_.FoundationModelIdentifier(agent_model_id),
        ).model_arn

        # The name for this role is a requirement for Bedrock
        agent_role = iam_.Role(
            scope=self,
            id="AgentRole",
            assumed_by=iam_.ServicePrincipal("bedrock.amazonaws.com"),
            role_name=f"{self.id}-AgentRole",
        )

        agent_role.add_to_policy(
            iam_.PolicyStatement(
                sid="InvokeModel",
                actions=["bedrock:InvokeModel"],
                effect=iam_.Effect.ALLOW,
                resources=[agent_model_arn],
            )
        )
        agent_role.add_to_policy(
            iam_.PolicyStatement(
                sid="RetrieveKB",
                actions=["bedrock:Retrieve"],
                effect=iam_.Effect.ALLOW,
                resources=[knowledge_base.attr_knowledge_base_arn],
            )
        )

        agent = bedrock_.CfnAgent(
            scope=self,
            id="Agent",
            agent_name=f"{self.id}-Agent",
            instruction=agent_instructions,
            agent_resource_role_arn=agent_role.role_arn,
            foundation_model=agent_model_id,
            knowledge_bases=[
                {
                    "description": "Main knowledge base",
                    "knowledgeBaseId": knowledge_base.attr_knowledge_base_id,
                }
            ],
        )

        agent_alias = bedrock_.CfnAgentAlias(
            scope=self,
            id="AgentAlias",
            agent_alias_name=agent_alias_name,
            agent_id=agent.attr_agent_id,
        )

        return agent, agent_alias

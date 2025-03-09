import json

from aws_cdk import CfnOutput, Stack
from aws_cdk import aws_opensearchserverless as aoss_
from aws_cdk import aws_ssm as ssm_
from constructs import Construct


def get_aoss_vpce_id(scope: Construct) -> str:
    return ssm_.StringParameter.value_for_string_parameter(
        scope, "/account/vpce-aoss/aossVpcEndpointId"
    )


class AossStack(Stack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        access_role_arns: list[str],
    ):
        super().__init__(scope, id)
        self.id = id

        collection = aoss_.CfnCollection(
            scope=self,
            id="AOSSCollection",
            name=f"{self.id.lower()}-collection",
            description=f"{self.id} Store",
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

        policy = json.dumps(
            [
                {
                    "Description": "Agent data policy",
                    "Principal": access_role_arns,
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


        CfnOutput(
            scope=self,
            id="CollectionId",
            value=collection.logical_id,
            description="The ID of the vector database collection",
        )

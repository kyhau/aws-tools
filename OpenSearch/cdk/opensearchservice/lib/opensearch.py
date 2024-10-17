"""
The OpenSearch service stack creates an Amazon OpenSearch Service domain with the following configuration:
- OpenSearch domain with data, master and ultra-warm nodes
- security groups
- KMS key and alias for encrypting the OpenSearch domain admin password
- Secret for the OpenSearch domain admin password is stored in Secrets Manager
"""
import random
import string

from aws_cdk import RemovalPolicy, SecretValue, Stack
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_opensearchservice as opensearch
from aws_cdk import aws_secretsmanager as sm
from constructs import Construct
from lib.base_infra import BaseInfra
from lib.kms import create_kms_key_and_alias

# OpenSearch specific constants, change this config if you would like you to change instance type, count and size
DOMAIN_ADMIN_PW = (
    "".join(
        random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
        for i in range(13)
    )
    + random.choice(string.ascii_lowercase)
    + random.choice(string.ascii_uppercase)
    + random.choice(string.digits)
    + "!"
)


class OpenSearchServiceStack(Stack):
    def __init__(self, scope: Construct, id: str, config: dict, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.config = config
        self.base_infra = BaseInfra(self, self.config["AppName"])
        self.app_name = f"{self.base_infra.base_stack_name}-opensearch"
        self.app_subnets = self.base_infra.app_subnets
        os_config = config["OpenSearch"]

        ################################################################################
        # Create secret for OpenSearch domain admin
        key_alias_name = f"alias/{self.app_name}"
        key_alias = create_kms_key_and_alias(
            self,
            id=f"{self.app_name}KmsKey",
            key_alias=key_alias_name,
            key_admin_arns=config["Kms"]["key_admin_arns"],
            key_user_arns_like=config["Kms"]["key_user_arns"],
        )
        secret = sm.Secret(
            self,
            id=f"{self.app_name}-secret",
            description=f"Secret for {self.app_name}",
            encryption_key=key_alias,
            secret_name=f"/apps/{self.app_name}/domain-admin-pw",
            secret_string_value=SecretValue.unsafe_plain_text(DOMAIN_ADMIN_PW),
        )
        secret.node.add_dependency(key_alias)

        ################################################################################
        # Amazon OpenSearch Service domain
        os_sg = ec2.SecurityGroup(
            self,
            f"{self.app_name}-sg",
            vpc=self.base_infra.app_vpc,
            allow_all_outbound=False,
            security_group_name=f"{self.app_name}-sg",
        )
        os_sg.add_ingress_rule(
            peer=ec2.Peer.ipv4(self.base_infra.app_subnet_cidr),
            connection=ec2.Port.tcp(443),
            description="Allow inbound HTTPS traffic from the app subnets",
        )
        os_sg.add_ingress_rule(
            peer=ec2.Peer.ipv4(self.base_infra.app_subnet_cidr),
            connection=ec2.Port.tcp(80),
            description="Allow inbound HTTP traffic from the app subnets",
        )

        _ = opensearch.Domain(
            self,
            f"{self.app_name}-domain",
            version=opensearch.EngineVersion.OPENSEARCH_2_15,  # Upgrade when CDK upgrades
            domain_name=self.app_name,
            removal_policy=RemovalPolicy.DESTROY,
            capacity=opensearch.CapacityConfig(
                data_node_instance_type=os_config["domain_data_node_instance_type"],
                data_nodes=os_config["domain_data_node_instance_count"],
                master_node_instance_type=os_config["domain_master_node_instance_type"],
                master_nodes=os_config["domain_master_node_instance_count"],
                warm_instance_type=os_config["domain_uw_node_instance_type"],
                warm_nodes=os_config["domain_uw_node_instance_count"],
            ),
            ebs=opensearch.EbsOptions(
                enabled=True,
                volume_size=os_config["domain_instance_volume_size"],
                volume_type=ec2.EbsDeviceVolumeType.GP3,
            ),
            vpc=self.base_infra.app_vpc,
            vpc_subnets=[ec2.SubnetSelection(subnets=self.app_subnets)],
            security_groups=[
                os_sg,
                self.base_infra.int_users_sg,
            ],
            zone_awareness=opensearch.ZoneAwarenessConfig(
                enabled=True, availability_zone_count=os_config["domain_az_count"]
            ),
            enforce_https=True,
            node_to_node_encryption=True,
            encryption_at_rest={"enabled": True},
            use_unsigned_basic_auth=True,
            fine_grained_access_control={
                "master_user_name": os_config["domain_admin_uname"],
                "master_user_password": SecretValue.unsafe_plain_text(DOMAIN_ADMIN_PW),
            },
            logging=opensearch.LoggingOptions(
                audit_log_enabled=True,
                slow_search_log_enabled=True,
                app_log_enabled=True,
                slow_index_log_enabled=True,
            ),
        )

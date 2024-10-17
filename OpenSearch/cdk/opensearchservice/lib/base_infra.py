import os

from aws_cdk import aws_ec2 as ec2
from aws_cdk.aws_ssm import StringParameter
from constructs import Construct

CDK_LOCAL_SYNC = os.environ.get("CDK_LOCAL_SYNC", "true").lower() == "true"  # with no credentials

AZS = ["ap-southeast-2"]
SUBNET_AZs = [
    "ap-southeast-2a",
    "ap-southeast-2b",
    "ap-southeast-2c",
]
SSM_PARAM_VPC01_ID = "/account/vpc01-id"
SSM_PARAM_VPC01_SUBNET_APP_IDs = [
    "/account/vpc01-subnet-app-a-id",
    "/account/vpc01-subnet-app-b-id",
    "/account/vpc01-subnet-app-c-id",
]
SSM_PARAM_VPC01_APP_CIDR = "/account/vpc01-app-cidr"
SSM_PARAM_VPC01_SG_INT_USERS_ID = "/account/vpc01-securitygroup-int-users-id"
SSM_PARAM_VPC01_ROUTE_TABLE_IDs = [
    "/account/vpc01-routetable-app-a-id",
    "/account/vpc01-routetable-app-b-id",
    "/account/vpc01-routetable-app-c-id",
]


class BaseInfra(Construct):
    def __init__(self, scope: Construct, app_name: str) -> None:
        super().__init__(scope, "BaseInfra")

        self.app_name = app_name
        self.base_stack_name = app_name.lower()

        self.app_subnet_ids = [
            self._value_from_lookup(ssm_param) for ssm_param in SSM_PARAM_VPC01_SUBNET_APP_IDs
        ]
        self.app_subnets = self.get_app_subnets(scope)

        self.vpc_id = self._value_from_lookup(SSM_PARAM_VPC01_ID)
        self.app_vpc = ec2.Vpc.from_vpc_attributes(
            self,
            "AppVpc",
            vpc_id=self.vpc_id,
            availability_zones=AZS,
            private_subnet_ids=self.app_subnet_ids,
        )

        self.app_subnet_cidr = self._value_from_lookup(
            SSM_PARAM_VPC01_APP_CIDR, mock_value="10.0.0.0/28"
        )

        self.int_users_sg = ec2.SecurityGroup.from_security_group_id(
            self,
            "InternalUsersSG",
            self._value_from_lookup(SSM_PARAM_VPC01_SG_INT_USERS_ID),
        )

    def get_app_subnets(self, scope: Construct, prefix: str = "default") -> list:
        app_subnets = []
        for i, subnet_id in enumerate(self.app_subnet_ids):
            route_table_id = self._value_from_lookup(SSM_PARAM_VPC01_ROUTE_TABLE_IDs[i])
            app_subnets.append(
                ec2.Subnet.from_subnet_attributes(
                    scope,
                    f"{prefix}AppSubnet{i}",
                    subnet_id=subnet_id,
                    availability_zone=SUBNET_AZs[i],
                    route_table_id=route_table_id,
                )
            )
        return app_subnets

    def _value_from_lookup(self, param_name: str, mock_value=None) -> str:
        if CDK_LOCAL_SYNC is True:
            return mock_value if mock_value else f'mock-{param_name.replace("/", "-")}'
        return StringParameter.value_from_lookup(self, param_name)

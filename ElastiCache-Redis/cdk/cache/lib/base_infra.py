import os

from aws_cdk import aws_ec2 as ec2
from aws_cdk.aws_ssm import StringParameter
from constructs import Construct

CDK_LOCAL_SYNC = os.environ.get("CDK_LOCAL_SYNC", "false").lower() == "true"  # with no credentials

AZS = ["ap-southeast-2"]
SSM_PARAM_VPC01_ID = "/account/vpc01-id"
SSM_PARAM_VPC01_SUBNET_APP_A_ID = "/account/vpc01-subnet-app-a-id"
SSM_PARAM_VPC01_SUBNET_APP_B_ID = "/account/vpc01-subnet-app-b-id"
SSM_PARAM_VPC01_SUBNET_APP_C_ID = "/account/vpc01-subnet-app-c-id"
SSM_PARAM_VPC01_SG_INT_USERS_ID = "/account/vpc01-securitygroup-int-users-id"
REDIS_PORT = 637


# BaseInfra class is a Construct that defines the base infrastructure for the application.
class BaseInfra(Construct):
    def __init__(self, scope: Construct, app_name: str) -> None:
        super().__init__(scope, "BaseInfra")

        self.app_name = app_name
        self.base_stack_name = app_name.lower()

        self.app_subnet_ids = [
            self._value_from_lookup(SSM_PARAM_VPC01_SUBNET_APP_A_ID),
            self._value_from_lookup(SSM_PARAM_VPC01_SUBNET_APP_B_ID),
            self._value_from_lookup(SSM_PARAM_VPC01_SUBNET_APP_C_ID),
        ]

        self.vpc_id = self._value_from_lookup(SSM_PARAM_VPC01_ID)
        self.app_vpc = ec2.Vpc.from_vpc_attributes(
            self,
            "AppVpc",
            vpc_id=self.vpc_id,
            availability_zones=AZS,
            private_subnet_ids=self.app_subnet_ids,
        )

        self.int_users_sg = ec2.SecurityGroup.from_security_group_id(
            self,
            "InternalUsersSG",
            self._value_from_lookup(SSM_PARAM_VPC01_SG_INT_USERS_ID),
        )

    def _value_from_lookup(self, param_name: str) -> str:
        if CDK_LOCAL_SYNC is True:
            return f'mock-{param_name.replace("/", "-")}'
        return StringParameter.value_from_lookup(self, param_name)

"""
Deploy an Arize Phoenix with local database, with a Fargate service with EFS, behind an ALB with custom DNS.
"""

from aws_cdk import CfnOutput, RemovalPolicy, Stack
from aws_cdk import aws_certificatemanager as acm
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_efs as efs
from aws_cdk import aws_elasticloadbalancingv2 as elbv2
from aws_cdk import aws_iam as iam
from aws_cdk import aws_route53 as r53
from aws_cdk import aws_route53_targets as r53_targets
from base_infra import BaseInfra
from constructs import Construct


class AlbFargate(Stack):
    def __init__(self, scope: Construct, id: str, config: dict, image: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.config = config
        self.base_infra = BaseInfra(self, self.config["AppName"])
        self.app_name = f"{self.base_infra.base_stack_name}-phoenix"
        self.app_subnets = self.base_infra.app_subnets

        self.vpc = self.base_infra.app_vpc

        fargate_efs = self.create_efs()

        alb, alb_sg = self.create_alb()

        cluster = self.create_cluster()

        task_def = self.create_task_def(image, fargate_efs)

        fargate_service = self.create_fargate_service(alb_sg, cluster, task_def)

        self.create_listener(fargate_service, alb)

        #  Allow access to EFS from Fargate ECS
        fargate_efs.grant_root_access(task_def.task_role.grant_principal)
        fargate_efs.connections.allow_default_port_from(fargate_service.connections)

        domain_name = self.create_custom_dns(alb)

        # Expose the ALB SG for updating the SG rules in other stacks
        self.alb_sg = alb_sg

        CfnOutput(self, "CustomDomainName", value=domain_name)
        CfnOutput(self, "LoadBalancerDNS", value=alb.load_balancer_dns_name)

    def create_cluster(self) -> ecs.Cluster:
        return ecs.Cluster(
            self,
            f"{self.app_name}-cluster",
            cluster_name=self.app_name,
            container_insights=True,
            vpc=self.base_infra.app_vpc,
        )

    def create_task_def(self, image, fargate_efs) -> ecs.FargateTaskDefinition:
        execution_role = iam.Role(
            self,
            id=f"{self.app_name}-execution-role",
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "service-role/AmazonECSTaskExecutionRolePolicy"
                )
            ],
        )

        task_role = iam.Role(
            self,
            f"{self.app_name}-task-role",
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
        )

        task_def = ecs.FargateTaskDefinition(
            self,
            id=f"{self.app_name}-task-def",
            cpu=256,
            memory_limit_mib=512,
            family=self.app_name,
            execution_role=execution_role,
            task_role=task_role,
        )
        task_def.add_container(
            id=f"{self.app_name}-container",
            image=ecs.ContainerImage.from_registry(image),
            memory_reservation_mib=512,
            logging=ecs.LogDrivers.aws_logs(stream_prefix="ecs"),
            port_mappings=[ecs.PortMapping(container_port=6006)],
            ulimits=[ecs.Ulimit(name=ecs.UlimitName.NOFILE, soft_limit=100000, hard_limit=100000)],
        )
        task_def.add_volume(
            name="efs",
            efs_volume_configuration=ecs.EfsVolumeConfiguration(
                file_system_id=fargate_efs.file_system_id
            ),
        )
        return task_def

    def create_fargate_service(self, alb_sg, cluster, task) -> ecs.FargateService:
        service_sg = ec2.SecurityGroup(
            self,
            f"{self.app_name}-service-sg",
            description=f"{self.app_name} Service SG",
            security_group_name=f"{self.app_name}-service-sg",
            vpc=self.base_infra.app_vpc,
        )
        service_sg.add_ingress_rule(
            peer=alb_sg, connection=ec2.Port.tcp(80), description="Load balancer to target"
        )

        fargate_service = ecs.FargateService(
            self,
            f"{self.app_name}-service",
            cluster=cluster,
            task_definition=task,
            desired_count=1,
            assign_public_ip=False,
            security_groups=[service_sg],
            vpc_subnets=ec2.SubnetSelection(subnets=self.app_subnets),
            service_name=f"{self.app_name}-service",
            enable_ecs_managed_tags=True,
            propagate_tags=ecs.PropagatedTagSource.TASK_DEFINITION,
        )
        return fargate_service

    def create_alb(self) -> tuple:
        alb_sg = ec2.SecurityGroup(
            self,
            id=f"{self.app_name}-alb-sg",
            allow_all_outbound=False,
            description=f"{self.app_name} ALB SG",
            security_group_name=f"{self.app_name}-alb-sg",
            vpc=self.base_infra.app_vpc,
        )
        alb = elbv2.ApplicationLoadBalancer(
            self,
            f"{self.app_name}-alb",
            vpc=self.base_infra.app_vpc,
            vpc_subnets=ec2.SubnetSelection(subnets=self.app_subnets),
            internet_facing=False,
            security_group=alb_sg,
            load_balancer_name=f"{self.app_name}-alb",
        )
        alb.add_security_group(self.base_infra.int_users_sg)
        return alb, alb_sg

    def create_listener(self, fargate_service, alb):
        certificate = acm.Certificate.from_certificate_arn(
            self,
            "HttpsFargateAlbCertificate",
            certificate_arn=self.base_infra.int_certificate_wildcard_arn,
        )

        listener = alb.add_listener("Listener", port=443, open=False, certificates=[certificate])
        listener.add_targets("EcsTargetGroup", port=80, targets=[fargate_service])

    def create_custom_dns(self, alb) -> str:
        domain_name = f"{self.app_name}.{self.base_infra.int_domain_name}"

        r53.ARecord(
            self,
            id=f"{self.app_name}-https-alb-arecord",
            record_name=domain_name,
            target=r53.RecordTarget.from_alias(r53_targets.LoadBalancerTarget(alb)),
            zone=self.base_infra.int_hosted_zone,
        )
        return domain_name

    def create_efs(self) -> efs.FileSystem:
        fileSystem = efs.FileSystem(
            self,
            id=f"{self.app_name}-efs",
            vpc=self.base_infra.app_vpc,
            encrypted=True,
            removal_policy=RemovalPolicy.RETAIN,
            performance_mode=efs.PerformanceMode.GENERAL_PURPOSE,
            throughput_mode=efs.ThroughputMode.BURSTING,
        )

        fileSystem.add_to_resource_policy(
            iam.PolicyStatement(
                actions=["elasticfilesystem:ClientMount"],
                principals=[iam.AnyPrincipal()],
                conditions={"Bool": {"elasticfilesystem:AccessedViaMountTarget": "true"}},
            )
        )
        return fileSystem

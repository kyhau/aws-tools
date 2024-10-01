from aws_cdk import Stack
from aws_cdk import aws_cloudwatch as cw
from aws_cdk import aws_cloudwatch_actions as cw_actions
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_elasticache as elasticache
from aws_cdk import aws_ssm as ssm
from constructs import Construct
from lib.base_infra import REDIS_PORT, BaseInfra


class RedisStack(Stack):
    def __init__(self, scope: Construct, id: str, config: dict, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.config = config
        self.base_infra = BaseInfra(self, app_name=self.config["AppName"])
        self.redis_port = ec2.Port.tcp(REDIS_PORT)
        self.redis, self.cache_sg = self.create_redis()
        self.create_ssm_parameters()
        self.redis_node_names = self.construct_redis_node_names()
        # TODO
        # self.redis_alarms = self.create_alarms()
        self.redis_namespace = "AWS/ElastiCache"

    def get_host(self) -> str:
        if self.redis.num_node_groups and self.redis.num_node_groups > 1:
            return self.redis.attr_configuration_end_point_address
        else:
            return self.redis.attr_primary_end_point_address

    def get_port(self) -> str:
        if self.redis.num_node_groups and self.redis.num_node_groups > 1:
            return self.redis.attr_configuration_end_point_port
        else:
            return self.redis.attr_primary_end_point_port

    def is_cluster(self) -> bool:
        return self.redis.num_node_groups and self.redis.num_node_groups > 1

    def create_ssm_parameters(self):
        ssm.StringParameter(
            self,
            "ParameterRedisNode0",
            parameter_name=f"/apps/{self.base_infra.base_stack_name}/redis.nodes",
            string_value=f"{self.redis.attr_primary_end_point_address}:{self.redis.attr_primary_end_point_port}",
        )

        params = self.config["Redis"]["parameter_store"]
        if params:
            for key, value in params.items():
                ssm.StringParameter(
                    self,
                    f"ParameterRedis{key}",
                    parameter_name=f"/apps/{self.base_infra.base_stack_name}/redis.{key}",
                    string_value=str(value),
                )

    def create_redis(self) -> dict:
        cache_sg = ec2.SecurityGroup(self, "RedisSecurityGroup", vpc=self.base_infra.app_vpc)

        subnet_group = elasticache.CfnSubnetGroup(
            self,
            f"{self.base_infra.app_name}RedisSubnetGroup",
            cache_subnet_group_name=f"{self.stack_name}SubnetGroup",
            subnet_ids=self.base_infra.app_subnet_ids,
            description="Redis subnet group for app layer",
        )

        auto_failover = False
        if (
            self.config["Redis"]["replicas_per_node_group"] > 0
            and self.config["Redis"]["multi_az_enabled"]
        ):
            auto_failover = True

        redis_replication = elasticache.CfnReplicationGroup(
            self,
            "RedisReplicaGroup",
            engine="redis",
            cache_node_type=self.config["Redis"]["instance_type"],
            replicas_per_node_group=self.config["Redis"]["replicas_per_node_group"],
            num_node_groups=self.config["Redis"]["num_node_groups"],
            automatic_failover_enabled=auto_failover,
            auto_minor_version_upgrade=True,
            replication_group_description=f"Redis Replication group for {self.base_infra.app_name}",
            cache_subnet_group_name=subnet_group.ref,
            replication_group_id=self.stack_name,
            security_group_ids=[
                cache_sg.security_group_id,
                self.base_infra.int_users_sg.security_group_id,
            ],
            at_rest_encryption_enabled=True,
            transit_encryption_enabled=True,
            transit_encryption_mode="preferred",
        )
        redis_replication.add_dependency(subnet_group)
        redis_replication.add_property_override(
            "MultiAZEnabled", self.config["Redis"]["multi_az_enabled"]
        )

        return redis_replication, cache_sg

    def create_alarms(self):
        alarms = []
        node_list = self.redis_node_names

        for node in node_list:
            redis_dimension = {"CacheClusterId": node}

            redis_memory_metric = cw.Metric(
                metric_name="DatabaseMemoryUsagePercentage",
                dimensions_map=redis_dimension,
                namespace=self.redis_namespace,
                label="DBUsagePercentage",
            )

            redis_memory_alarm = redis_memory_metric.create_alarm(
                self,
                f"{node}MemoryUsageAlarm",
                threshold=self.config["Redis"]["alarms"]["memory_usage_error"],
                evaluation_periods=2,
            )

            redis_memory_warn = redis_memory_metric.create_alarm(
                self,
                f"{node}MemoryUsageWarn",
                threshold=self.config["Redis"]["alarms"]["memory_usage_warning"],
                evaluation_periods=2,
            )

            redis_memory_alarm.add_alarm_action(cw_actions.SnsAction(self.shared_stack.alert_topic))
            redis_memory_alarm.add_ok_action(cw_actions.SnsAction(self.shared_stack.alert_topic))

            redis_memory_warn.add_alarm_action(
                cw_actions.SnsAction(self.shared_stack.notification_topic)
            )
            redis_memory_warn.add_ok_action(
                cw_actions.SnsAction(self.shared_stack.notification_topic)
            )

            alarms.append(redis_memory_alarm)
            alarms.append(redis_memory_warn)

        return alarms

    def construct_redis_node_names(self):
        replica_list = self.get_redis_replica_num()
        node_group_list = self.get_redis_node_group_num()
        prefix = self.redis.replication_group_id

        node_name_list = []

        if node_group_list:
            for num in node_group_list:
                for r in replica_list:
                    node_name = f"{prefix}-{num}-{r}"
                    node_name_list.append(node_name)
        else:
            for r in replica_list:
                node_name = f"{prefix}-{r}"
                node_name_list.append(node_name)

        return node_name_list

    def get_redis_node_group_num(self):
        num_list = []
        if self.redis.num_node_groups and self.redis.num_node_groups > 1:
            for i in range(1, self.redis.num_node_groups + 1):
                num_list.append(str(i).zfill(4))
        return num_list

    def get_redis_replica_num(self):
        num_list = []
        if self.redis.replicas_per_node_group and self.redis.replicas_per_node_group > 0:
            for i in range(self.redis.replicas_per_node_group + 1):
                num_list.append(str(i + 1).zfill(3))
        else:
            num_list.append(str(1).zfill(3))
        return num_list

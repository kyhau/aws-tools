#!/usr/bin/env python3
from os.path import dirname, join, realpath

import yaml
from aws_cdk import App, Environment, Tags
from lib.redis import RedisStack

ENV_DIR = join(dirname(realpath(__file__)), "environment")


def main():
    app = App()

    ENV_NAME = app.node.try_get_context("env") or "dev"

    with open(join(ENV_DIR, f"{ENV_NAME}.yml"), "r") as stream:
        yaml_data = yaml.safe_load(stream)
        config = yaml_data if yaml_data is not None else {}

    app_name = config["AppName"]

    redis_stack = RedisStack(
        scope=app,
        id=f"{app_name}-Redis",
        config=config,
        env=Environment(account=config["Account"], region=config["Region"]),
    )
    # redis_stack.cache_sg.add_ingress_rule(
    #     peer=fargate_stack.task_security_group,
    #     connection=ec2.Port.tcp(REDIS_PORT),
    #     description="Allow inbound traffic from the Task SG",
    # )

    for key, value in config["Tags"].items():
        Tags.of(redis_stack).add(key, value)

    app.synth()


if __name__ == "__main__":
    main()

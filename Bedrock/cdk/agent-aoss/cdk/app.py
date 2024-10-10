#!/usr/bin/env python3
from os.path import dirname, join, realpath

import yaml
from aws_cdk import App, CliCredentialsStackSynthesizer, Environment, Tags
from aws_cdk.aws_logs import RetentionDays
from backend.bedrock_agent_stack import BedrockAgentStack

ENV_DIR = join(dirname(dirname(realpath(__file__))), "environment")


def main():
    app = App()

    ENV_NAME = app.node.try_get_context("env") or "dev"

    with open(join(ENV_DIR, f"{ENV_NAME}.yml"), "r") as stream:
        yaml_data = yaml.safe_load(stream)
        config = yaml_data if yaml_data is not None else {}

    config["LogRetentionInDays"] = (
        RetentionDays.ONE_MONTH if ENV_NAME == "prd" else RetentionDays.ONE_DAY
    )

    app_name = config["AppName"]

    stack = BedrockAgentStack(
        scope=app,
        id=f"{app_name}",
        config=config,
        env=Environment(account=config["Account"], region=config["Region"]),
        description=f"{app_name} GenAI Assistant",
        synthesizer=CliCredentialsStackSynthesizer(),
        termination_protection=(ENV_NAME == "prd"),
    )

    for key, value in config["Tags"].items():
        Tags.of(stack).add(key, value)

    app.synth()


if __name__ == "__main__":
    main()

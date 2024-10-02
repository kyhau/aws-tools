#!/usr/bin/env python3
from os import environ
from os.path import dirname, join, realpath

import yaml
from aws_cdk import App, CliCredentialsStackSynthesizer, Environment, Tags
from lib.secrets import SecretsStack

ENV_DIR = join(dirname(realpath(__file__)), "environment")


def retrieve_secrets_from_env(secrets: dict) -> dict:
    for secret_name, item in secrets.items():
        if environ.get(secret_name) is None:
            raise ValueError(f"Missing secret {secret_name} in environment")
        secrets[secret_name]["value"] = environ[secret_name]
    return secrets


def main():
    app = App()

    ENV_NAME = app.node.try_get_context("env") or "dev"

    with open(join(ENV_DIR, f"{ENV_NAME}.yml"), "r") as stream:
        yaml_data = yaml.safe_load(stream)
        config = yaml_data if yaml_data is not None else {}

    app_name = config["AppName"]

    secrets = retrieve_secrets_from_env(config["Secrets"]["env"])
    is_single_object_secret = config["Secrets"].get("is-single-object-secret", False)

    # TODO retrieve from other stack
    key_user_arn_pattern_list = [
        "arn:aws:iam::*:role/TODO*",
    ]

    secrets_stack = None
    if environ.get("SECRET_1"):
        # Do not interact with this cdk stack if secret value is not provided (e.g., local env)
        secrets_stack = SecretsStack(
            scope=app,
            id=f"{app_name}-Secrets",
            app_name=app_name,
            secrets=secrets,
            is_single_object_secret=is_single_object_secret,
            key_admin_arn_list=config["Kms"]["key-admin-arns"],
            key_user_arn_pattern_list=key_user_arn_pattern_list,
            env=Environment(account=config["Account"], region=config["Region"]),
            description=f"{app_name} Secrets",
            synthesizer=CliCredentialsStackSynthesizer(),
            termination_protection=(ENV_NAME == "prd"),
        )

    # Add common tags
    stacks = []
    if secrets_stack:
        stacks.append(secrets_stack)

    for stack in stacks:
        for key, value in config["Tags"].items():
            Tags.of(stack).add(key, value)

    app.synth()


if __name__ == "__main__":
    main()

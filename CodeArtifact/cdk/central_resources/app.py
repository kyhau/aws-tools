#!/usr/bin/env python3
from os.path import dirname, join, realpath

import yaml
from aws_cdk import App, CliCredentialsStackSynthesizer, Environment, Tags
from cdklabs.cdk_validator_cfnguard import CfnGuardValidator
from lib.central_resources import CodeArtifactCentralResources

ENV_DIR = join(dirname(realpath(__file__)), "environment")


def main():
    app = App(
        policy_validation_beta1=[
            CfnGuardValidator(
                # By default the CfnGuardValidator plugin has the Control Tower proactive
                # rules enabled. If you wish to disable them, set this to false.
                control_tower_rules_enabled=True,
                # You can also disable individual rules by passing in a list of rule names
                # e.g. "ct-s3-pr-1" list is https://github.com/cdklabs/cdk-validator-cfnguard
                disabled_rules=[],
                # You can also pass in a list of local guard files or directory paths
                # e.g. "./guards", "./guards/custom-guard-file.guard"
                rules=[],
            )
        ]
    )

    ENV_NAME = app.node.try_get_context("env") or "dev"

    with open(join(ENV_DIR, f"{ENV_NAME}.yml"), "r") as stream:
        yaml_data = yaml.safe_load(stream)
        config = yaml_data if yaml_data is not None else {}

    stack = CodeArtifactCentralResources(
        scope=app,
        id="CodeArtifactCentralResources",
        config=config,
        env=Environment(
            account=config["AWS_ACCOUNT"],
            region=config["AWS_REGION"],
        ),
        synthesizer=CliCredentialsStackSynthesizer(),
        termination_protection=(ENV_NAME == "prd"),
    )

    # Add common tags
    for key, value in config["TAGS"].items():
        Tags.of(stack).add(key, value)

    Tags.of(stack).add("Description", "CodeArtifact central resources")
    Tags.of(stack).add("Environment", ENV_NAME)
    Tags.of(stack).add("Name", stack.stack_name)

    app.synth()


if __name__ == "__main__":
    main()

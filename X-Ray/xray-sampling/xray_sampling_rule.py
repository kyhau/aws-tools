"""
A simple helper for creating/updating/deleting x-ray sampling rule.
"""
import json

import click
from boto3.session import Session


def print_response(response):
    print(f'HTTPStatusCode: {response["ResponseMetadata"]["HTTPStatusCode"]}')
    print(json.dumps(response["SamplingRuleRecord"], indent=2, default=str))


class Helper:
    def __init__(self, session, region) -> None:
        self.client = session.client('xray', region_name=region)

    def get_sampling_rules(self, rule_name=None):
        params = {}
        for page in self.client.get_paginator('get_sampling_rules').paginate(**params).result_key_iters():
            for item in page:
                if rule_name == item['SamplingRule']['RuleName']:
                    return item['SamplingRule']
                print(json.dumps(item['SamplingRule'], indent=2))

    def export_rule_to_file(self, rule_name):
        rule = self.get_sampling_rules(rule_name)
        if rule is None:
            print(f'Rule {rule_name} not found')
        else:
            outfile = f'{rule_name}.json'
            with open(outfile, 'w') as f:
                json.dump(rule, f, indent=2)
                print(f'Output file: {outfile}')

    def create_sampling_rule(self, input_json_file):
        with open(input_json_file, 'r') as f:
            data = json.load(f)

        if data.get('Version') is None:
            data['Version'] = 1

        try:
            resp = self.client.create_sampling_rule(SamplingRule=data)
            print_response(resp)
        except Exception as e:
            print(e)

    def delete_sampling_rule(self, rule_name):
        resp = self.client.delete_sampling_rule(RuleName=rule_name)
        print_response(resp)

    def update_sampling_rule(self, input_json_file):
        with open(input_json_file, 'r') as f:
            data = json.load(f)

        for key in ['RuleARN', 'Version']:
            if data.get(key):
                del data[key]

        try:
            resp = self.client.update_sampling_rule(SamplingRuleUpdate=data)
            print_response(resp)
        except Exception as e:
            print(e)


@click.group(help='A helper class to manage x-ray sampling rule quickly.')
@click.option('--profile', '-p', default='default', show_default=True, help='AWS profile name')
@click.option('--region', '-r', default='ap-southeast-2', show_default=True, help='AWS region')
@click.pass_context
def cli_main(ctx, profile, region):
    session = Session(profile_name=profile)
    ctx.obj = {'session': session, 'region': region}


@cli_main.command(help='List all x-ray sampling rules.')
@click.pass_context
def ls(ctx):
    Helper(ctx.obj['session'], ctx.obj['region']).get_sampling_rules()


@cli_main.command(help='Export a rule to a local file (rule_name.json).')
@click.argument('rule_name')
@click.pass_context
def export(ctx, rule_name):
    Helper(ctx.obj['session'], ctx.obj['region']).export_rule_to_file(rule_name)


@cli_main.command(help='Create a new sampling rule with the given input json file.')
@click.argument('input_json_file')
@click.pass_context
def create(ctx, input_json_file):
    Helper(ctx.obj['session'], ctx.obj['region']).create_sampling_rule(input_json_file)


@cli_main.command(help='Delete the sampling rule of the given rule name.')
@click.argument('rule_name')
@click.pass_context
def delete(ctx, rule_name):
    Helper(ctx.obj['session'], ctx.obj['region']).delete_sampling_rule(rule_name)


@cli_main.command(help='Update an existing sampling rule with the given input json file.')
@click.argument('input_json_file')
@click.pass_context
def update(ctx, input_json_file):
    Helper(ctx.obj['session'], ctx.obj['region']).update_sampling_rule(input_json_file)


if __name__ == '__main__':
    cli_main(obj={})

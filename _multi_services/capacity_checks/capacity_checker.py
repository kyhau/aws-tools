"""
Check capacity of scalable AWS resources
Author/Maintainer: kyhau
"""
import json
import logging
from collections import defaultdict
from datetime import datetime
from os import makedirs
from os.path import basename, join

import click
from boto3.session import Session

logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('urllib3.connectionpool').setLevel(logging.CRITICAL)

OUTPUT_DIR = 'capacity_reports'
makedirs(OUTPUT_DIR, exist_ok=True)

current_dt = datetime.now().strftime('%Y-%m-%d %H:%M AEST')


def get_tag_value(tags, key='Name'):
    for tag in tags:
        if tag['Key'] == key:
            return tag['Value']
    return None


def check_asg(session, stack_profile, physical_id):
    try:
        client = session.client('autoscaling')
        obj = client.describe_auto_scaling_groups(AutoScalingGroupNames=[physical_id])['AutoScalingGroups'][0]

        mixed_instances_policy = obj.get('MixedInstancesPolicy', {}).get('LaunchTemplate', {}).get('Overrides')

        ret = {
            'AZs': {},
            'CheckTime': current_dt,
            'Desired': obj['DesiredCapacity'],
            'MinSize': obj['MinSize'],
            'MaxSize': obj['MaxSize'],
            'InstanceCount': 0,
            'InstanceTypes': {},
            'MixedInstancesPolicy': [v['InstanceType'] for v in mixed_instances_policy] if mixed_instances_policy else None
        }

        client = session.client('ec2')
        params = {'Filters': [{'Name': 'tag:aws:autoscaling:groupName', 'Values': [physical_id]}]}

        for page in client.get_paginator('describe_instances').paginate(**params).result_key_iters():
            for obj in page:
                for instance in obj['Instances']:
                    instance_az = instance['Placement']['AvailabilityZone']
                    if instance_az not in ret['AZs']:
                        ret['AZs'][instance_az] = 0
                    ret['AZs'][instance_az] += 1

                    instance_type = instance['InstanceType']
                    if instance_type not in ret['InstanceTypes']:
                        ret['InstanceTypes'][instance_type] = 0
                    ret['InstanceTypes'][instance_type] += 1
                    ret['InstanceCount'] += 1

        if 'AsgActual' not in stack_profile['Actual']:
            stack_profile['Actual']['AsgActual'] = {}
        stack_profile['Actual']['AsgActual'][physical_id] = ret

    except Exception as e:
        logging.error(f'Not found {physical_id}: {e}')


def check_ec2(session, stack_profile, physical_id):
    try:
        client = session.client('ec2')
        ret = stack_profile['Actual'].get('Ec2Actual')
        if ret is None:
            ret = {
                'AZs': {},
                'CheckTime': current_dt,
                'InstanceCount': 0,
                'InstanceTypes': {},
            }

        instance = client.describe_instances(InstanceIds=[physical_id])['Reservations'][0]['Instances'][0]

        instance_az = instance['Placement']['AvailabilityZone']
        if instance_az not in ret['AZs']:
            ret['AZs'][instance_az] = 0
        ret['AZs'][instance_az] += 1

        instance_type = instance['InstanceType']
        if instance_type not in ret['InstanceTypes']:
            ret['InstanceTypes'][instance_type] = 0
        ret['InstanceTypes'][instance_type] += 1
        ret['InstanceCount'] += 1

        stack_profile['Actual']['Ec2Actual'] = ret

    except Exception as e:
        logging.error(f'Not found {physical_id}: {e}')


def check_ecs(session, stack_profile, physical_id):
    try:
        client = session.client('ecs')
        resp = client.describe_clusters(clusters=[physical_id])['clusters'][0]

        fargate_only = True
        try:
            task_arns = client.list_tasks(cluster=resp['clusterArn'])['taskArns']
            for task in client.describe_tasks(cluster=resp['clusterArn'], tasks=task_arns)['tasks']:
                if task['launchType'] != 'FARGATE':
                    fargate_only = False
        except Exception as e:
            logging.error(f'{physical_id}: {e}')

        ret = {
            'CheckTime': current_dt,
            'FargateOnly': fargate_only,
            'RegisteredContainerInstancesCount': resp['registeredContainerInstancesCount'],
            'RunningTasksCount': resp['runningTasksCount'],
        }

        if 'EcsClusterActual' not in stack_profile['Actual']:
            stack_profile['Actual']['EcsClusterActual'] = {}
        stack_profile['Actual']['EcsClusterActual'][physical_id] = ret

    except Exception as e:
        logging.error(f'Not found {physical_id}: {e}')


def check_rds_cluster(session, stack_profile, physical_id):
    try:
        client = session.client('rds')
        resp = client.describe_db_clusters(DBClusterIdentifier=physical_id)['DBClusters'][0]
        ret = {
            'AZs': {},
            'CheckTime': current_dt,
            'EngineMode': resp['EngineMode'],
            'InstanceCount': len(resp['DBClusterMembers']),
            'InstanceTypes': {},
            'MultiAZ': resp['MultiAZ'],
        }

        for member in resp['DBClusterMembers']:
            instance = client.describe_db_instances(DBInstanceIdentifier=member['DBInstanceIdentifier'])['DBInstances'][0]

            instance_az = instance['AvailabilityZone']
            if instance_az not in ret['AZs']:
                ret['AZs'][instance_az] = 0
            ret['AZs'][instance_az] += 1

            instance_type = instance['DBInstanceClass']
            if instance_type not in ret['InstanceTypes']:
                ret['InstanceTypes'][instance_type] = 0
            ret['InstanceTypes'][instance_type] += 1

        if 'RdsClusterActual' not in stack_profile['Actual']:
            stack_profile['Actual']['RdsClusterActual'] = {}
        stack_profile['Actual']['RdsClusterActual'][physical_id] = ret

    except Exception as e:
        logging.error(f'Not found {physical_id}: {e}')


def check_rds(session, stack_profile, physical_id):
    try:
        client = session.client('rds')
        instance = client.describe_db_instances(DBInstanceIdentifier=physical_id)['DBInstances'][0]
        if instance.get('DBClusterIdentifier') is not None:
            return

        ret = stack_profile['Actual'].get('RdsActual')
        if ret is None:
            ret = {
                'AZs': {},
                'CheckTime': current_dt,
                'InstanceCount': 0,
                'InstanceTypes': {},
            }

        instance_az = instance['AvailabilityZone']
        if instance_az not in ret['AZs']:
            ret['AZs'][instance_az] = 0
        ret['AZs'][instance_az] += 1

        instance_type = instance['DBInstanceClass']
        if instance_type not in ret['InstanceTypes']:
            ret['InstanceTypes'][instance_type] = 0
        ret['InstanceTypes'][instance_type] += 1
        ret['InstanceCount'] += 1

        stack_profile['Actual']['RdsActual'] = ret

    except Exception as e:
        logging.error(f'Not found {physical_id}: {e}')


def list_stacks(session):
    try:
        ret = []
        for page in session.client('cloudformation').get_paginator('list_stacks').paginate().result_key_iters():
            for stack in page:
                ret.append(stack['StackName'])
        return ret
    except Exception as e:
        if 'ValidationError' not in str(e):
            logging.error(e)


def get_stack_resources(session, stack_name):
    try:
        return session.client('cloudformation').describe_stack_resources(StackName=stack_name)['StackResources']
    except Exception as e:
        if 'ValidationError' not in str(e):
            logging.error(e)


def get_stack_project_tag(session, stack_name):
    try:
        stack_data = session.client('cloudformation').describe_stacks(StackName=stack_name)['Stacks'][0]
        return get_tag_value(stack_data['Tags'], key='Project')
    except Exception as e:
        if 'ValidationError' not in str(e):
            logging.error(e)


def process_account_stacks(session, account, account_capacity_resultset):
    for stack_name, stack_profile in account_capacity_resultset.items():
        stack_resources = get_stack_resources(session, stack_name)
        if stack_resources is None:
            continue

        account_capacity_resultset[stack_name]['Actual'] = {}
        account_capacity_resultset[stack_name]['Project'] = \
            account_capacity_resultset[stack_name].get(
                'Project', get_stack_project_tag(session, stack_name))

        for stack_resource in stack_resources:
            resource_type = stack_resource['ResourceType']
            physical_id = stack_resource.get('PhysicalResourceId')
            if physical_id is None:
                print('physical_id is None. Skipped')
                continue

            if resource_type == 'AWS::AutoScaling::AutoScalingGroup':
                print('Processing', account, stack_name, physical_id, resource_type)
                check_asg(session, stack_profile, physical_id)

            elif resource_type == 'AWS::ECS::Cluster':
                print('Processing', account, stack_name, physical_id, resource_type)
                check_ecs(session, stack_profile, physical_id)

            elif resource_type == 'AWS::EC2::Instance':
                print('Processing', account, stack_name, physical_id, resource_type)
                check_ec2(session, stack_profile, physical_id)

            elif resource_type == 'AWS::RDS::DBCluster':
                print('Processing', account, stack_name, physical_id, resource_type)
                check_rds_cluster(session, stack_profile, physical_id)

            elif resource_type == 'AWS::RDS::DBInstance':
                print('Processing', account, stack_name, physical_id, resource_type)
                check_rds(session, stack_profile, physical_id)

            elif resource_type in [
                'AWS::ElasticLoadBalancing::LoadBalancer',
                'AWS::ElasticLoadBalancingV2::LoadBalancer',
            ]:
                print('Processing', account, stack_name, physical_id, resource_type)
                stack_profile['Actual']['ElbActual'] = {physical_id: {'LCU': 0}}

            #TODO
            #elif resource_type == 'AWS::ElastiCache::CacheCluster':
            else:
                #print('TODO', stack_name, physical_id, resource_type)
                #print(json.dumps(stack_resource, indent=2, default=str))
                pass


@click.command(help='Check current capacity of scalable resources')
@click.argument('stack_file')
@click.option('--profile', '-p', default='default', show_default=True, help='AWS Profile name')
def main(stack_file, profile):

    with open(stack_file, 'r') as f:
        lines = [x.strip() for x in f.readlines()]
    account_capacity_resultset = {x: defaultdict(dict) for x in lines if x}

    account_name = basename(stack_file).split('.')[0]

    try:
        session = Session(profile_name=profile)
        process_account_stacks(session, account_name, account_capacity_resultset)

        # Cleanup
        to_be_delete = []
        for stack_name in account_capacity_resultset.keys():
            if account_capacity_resultset[stack_name].get('Actual') in [{}, None]:
                to_be_delete.append(stack_name)

        for stack_name in to_be_delete:
            del account_capacity_resultset[stack_name]

    finally:
        output_file = join(OUTPUT_DIR, f'{account_name}.json')
        with open(output_file, 'w') as f:
            json.dump(account_capacity_resultset, f, indent=2, sort_keys=True)


if __name__ == '__main__':
     main()

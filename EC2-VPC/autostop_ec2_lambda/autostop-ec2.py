#!/usr/bin/env python
from __future__ import absolute_import
import argparse
import boto3


# App defaults
DEFAULTS = {
    'ec2_regions': ['ap-southeast-2'],
    'autostop_tag_key': 'AutoStop'
}

class StopAllEC2(object):

    def __init__(self, profile_name=None):
        self._loaded = False
        self.profile_name = profile_name
        self.ec2_regions = list()
        self.autostop_tag_key = DEFAULTS['autostop_tag_key']

    def _load_config(self):
        if self._loaded:
            return

        parser = argparse.ArgumentParser(description='Create backups for EC2 instances with Tag [Service]')
        parser.add_argument('--regions', metavar='region', nargs='*',
                            help='EC2 Region(s) to process for snapshots',
                            default=DEFAULTS['ec2_regions'])
        settings = parser.parse_args()

        for region in settings.regions:
            self.ec2_regions.append(region)

        self._loaded = True

    def configure_from_lambda_event(self, event_details):
        for setting in DEFAULTS.keys():
            if setting in event_details:
                self.__setattr__(setting, event_details[setting])
            else:
                self.__setattr__(setting, DEFAULTS[setting])
        self._loaded = True

    def start_process(self):
        self._load_config()
        for region in self.ec2_regions:
            self.stop_all_vms(region)

    def stop_all_vms(self, region):
        """
        Stopping all running VMs (with a tag AutoStop=True) in a region of all aws
        accounts defined in profiles
        """
        try:
            ec2_client = self.ec2_resource(region=region, profile_name=self.profile_name)

            # find all ec2 instances which are tagged as 'vm'
            ret = ec2_client.instances.filter(
                Filters=[
                    {'Name': 'tag:Service', 'Values': ['vm']},
                    {'Name': 'tag:{}'.format(self.autostop_tag_key), 'Values': ['True']}
                ]
            ).stop()

            for r in ret:
                if 'StoppingInstances' in r.keys():
                    checked_instances = r['StoppingInstances']
                    for i in checked_instances:
                        if i['PreviousState']['Name'] in ['pending', 'running'] \
                                and i['CurrentState']['Name'] in ['stopped', 'stopping']:
                            print('{} has been stopped'.format(i['InstanceId']))
                        elif i['PreviousState']['Name'] in ['pending', 'running']:
                            print('{} has been stopped and current status is {}'.format(
                                i['InstanceId'], i['CurrentState']['Name']))

        except Exception as e:
            print('Error: Failed to stop all VM EC2 instances')
            print(e)

    @staticmethod
    def ec2_resource(region, profile_name=None):
        """
        Return a EC2 client
        """
        if profile_name is None:
            ec2 = boto3.resource('ec2', region_name=region)
        else:
            session = boto3.session.Session(profile_name=profile_name)
            ec2 = session.resource('ec2', region)
        return ec2


def lambda_handler(event, context):
    """
    Entry point for triggering from a AWS Lambda job
    """
    helper = StopAllEC2()
    helper.configure_from_lambda_event(event)
    helper.start_process()


if __name__ == '__main__':
    """
    Entry point for running from command line
    """
    # TODO change profile_name
    helper = StopAllEC2(profile_name='default-profile')
    helper.start_process()

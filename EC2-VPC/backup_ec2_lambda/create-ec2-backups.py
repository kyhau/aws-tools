#!/usr/bin/env python
from __future__ import absolute_import
import argparse
import boto3
import datetime


# App defaults
DEFAULTS = {
    'ec2_regions': ['ap-southeast-2'],
    'backup_tag': 'daily'
}

TAG_KEY_SERVICE = 'Service'
TAG_KEY_AUTOSNAP_ID = 'EC2-Snapper-Instance-ID'
TAG_KEY_AUTOSNAP_LABEL = 'EC2-Snapper-Label'
TAG_KEY_BILLING = 'Billing'

DATETIME_STR_FORMAT_1 = '%Y-%m-%d-%H-%M-%S'
DATETIME_STR_FORMAT_2 = '%Y-%m-%dT%H:%M:%S.000z'


class CreateEC2Backups(object):

    def __init__(self, profile_name=None):
        self._loaded = False
        self.profile_name = profile_name
        self.ec2_regions = list()
        self.backup_tag = DEFAULTS['backup_tag']

    def _load_config(self):
        if self._loaded:
            return

        parser = argparse.ArgumentParser(description='Create backups for EC2 instances with Tag [Service]')
        parser.add_argument('--regions', metavar='region', nargs='*',
                            help='EC2 Region(s) to process for snapshots',
                            default=DEFAULTS['ec2_regions'])
        parser.add_argument('--backup_tag', dest='backup_tag',
                            default=DEFAULTS['backup_tag'], metavar='TAG',
                            help='The tag to be added for categorising the backup (defaults to "daily".')
        settings = parser.parse_args()

        for region in settings.regions:
            self.ec2_regions.append(region)
        self.backup_tag = settings.backup_tag

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
            self.create_new_backups(region)

    def create_new_backups(self, region):
        """
        Create new backups (AMI and snapshots) for EC2 with tag "Service"
        """
        self._load_config()

        ec2_resource = self.ec2_resource(region=region, profile_name=self.profile_name)

        instances = ec2_resource.instances.all()
        for instance in instances:
            print('------------------------------------------------------------')
            print('Creating new AMI and snapshot for {} ...'.format(instance.id))

            i_name = instance.id
            i_bill = 'unknown'
            i_service_tag = None
            for i_tag in instance.tags:
                if i_tag['Key'] == TAG_KEY_SERVICE:
                    if i_tag['Value'] == '':
                        break
                    i_service_tag = i_tag['Value']
                elif i_tag['Key'] == 'Name':
                    i_name = i_tag['Value']
                elif i_tag['Key'] == TAG_KEY_BILLING:
                    i_bill = i_tag['Value']

            if i_service_tag is None:
                continue

            curr_datetime = datetime.datetime.now()
            ami_name = '{}-{}'.format(i_name, curr_datetime.strftime(DATETIME_STR_FORMAT_1))

            client = self.ec2_client(region=region, profile_name=self.profile_name)

            # create AMI
            ami_id = self.create_ami(client, instance.id, ami_name)
            if ami_id is None:
                continue

            # create tags
            self.create_tags(client, [ami_id], instance.id, ami_name, self.backup_tag, i_bill)

    @staticmethod
    def ec2_client(region, profile_name=None):
        """
        Return a EC2 client
        """
        if profile_name is None:
            ec2 = boto3.client('ec2', region_name=region)
        else:
            session = boto3.session.Session(profile_name=profile_name)
            ec2 = session.client('ec2', region)
        return ec2

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

    @staticmethod
    def create_ami(client, instance_id, image_name):
        print('Creating AMI ({}) for {} ...'.format(image_name, instance_id))
        try:
            response = client.create_image(
                InstanceId=instance_id,
                Name=image_name,
                Description=image_name,
                NoReboot=True
            )
            ami_id = response['ImageId']
            print('Created AMI with ID {}'.format(ami_id))
            return ami_id

        except Exception as e:
            print('Error: Failed to create AMI ({}) for {}'.format(image_name, instance_id))
            print(e)
        return None

    @staticmethod
    def create_tags(client, resource_id_list, instance_id, ami_name, backup_tag, billing):
        print('Creating tags for {} ...'.format(resource_id_list))
        try:
            response = client.create_tags(
                Resources=resource_id_list,
                Tags=[
                    {'Key': 'Name', 'Value': ami_name},
                    {'Key': TAG_KEY_AUTOSNAP_ID, 'Value': instance_id},
                    {'Key': TAG_KEY_AUTOSNAP_LABEL, 'Value': backup_tag},
                    {'Key': TAG_KEY_BILLING, 'Value': billing},
                ]
            )
            print('Tag {} created with value {}'.format(TAG_KEY_AUTOSNAP_ID, instance_id))
            print('Tag {} created with value {}'.format(TAG_KEY_AUTOSNAP_LABEL, backup_tag))
            print('Tag {} created with value {}'.format(TAG_KEY_BILLING, billing))
            return True

        except Exception as e:
            print('Error: Failed to create tags for {}'.format(resource_id_list))
            print(e)
        return False


def lambda_handler(event, context):
    """
    Entry point for triggering from a AWS Lambda job
    """
    helper = CreateEC2Backups()
    helper.configure_from_lambda_event(event)
    helper.start_process()


if __name__ == '__main__':
    """
    Entry point for running from command line
    """
    # TODO change profile_name
    helper = CreateEC2Backups(profile_name='default-profile')
    helper.start_process()

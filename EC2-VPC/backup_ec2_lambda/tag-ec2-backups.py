#!/usr/bin/env python
from __future__ import absolute_import
import argparse
import boto3
import datetime


# App defaults
DEFAULTS = {
    'ec2_regions': ['ap-southeast-2'],
    'backup_tag': 'daily',
}

TAG_KEY_SERVICE = 'Service'
TAG_KEY_AUTOSNAP_ID = 'EC2-Snapper-Instance-ID'
TAG_KEY_AUTOSNAP_LABEL = 'EC2-Snapper-Label'
TAG_KEY_BILLING = 'Billing'

DATETIME_STR_FORMAT_2 = '%Y-%m-%dT%H:%M:%S.000z'


class AwsTaggingHelper(object):

    def __init__(self, profile_name=None):
        self._loaded = False
        self.profile_name = profile_name
        self.ec2_regions = list()
        self.backup_tag = DEFAULTS['backup_tag']

    def _load_config(self):
        if self._loaded:
            return

        parser = argparse.ArgumentParser(description='Tag EC2 backups')
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
            self.tag_ami_backups(region)

    def tag_ami_backups(self, region):
        """
        Tag new backups
        """
        self._load_config()

        client = self.ec2_client(region=region, profile_name=self.profile_name)

        # find all AMIs having tag "EC2-Snapper-Label" = backup_tag
        response = client.describe_images(Filters=[{
            'Name': 'tag:{}'.format(TAG_KEY_AUTOSNAP_LABEL),
            'Values': [self.backup_tag]
        }])

        today = datetime.datetime.utcnow()

        for image in response['Images']:
            image_date = datetime.datetime.strptime(image['CreationDate'], DATETIME_STR_FORMAT_2)

            if today - image_date > datetime.timedelta(days=1):
                continue

            ami_id = image['ImageId']
            ami_name = image['Name']
            ami_bill = ''
            instance_id = ami_id
            for tag in image['Tags']:
                if tag['Key'] == TAG_KEY_AUTOSNAP_ID:
                    instance_id = tag['Value']
                elif tag['Key'] == TAG_KEY_BILLING:
                    ami_bill = tag['Value']

            print('------------------------------------------------------------')
            print('Started tagging snapshots of AMI {} (for {}) ...'.format(ami_id, instance_id))

            snapshot_ids = self.retrieve_snapshot_ids(client, ami_id)
            self.create_tags(client, snapshot_ids, instance_id, ami_name, self.backup_tag, ami_bill)

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
    def retrieve_snapshot_ids(client, ami_id):
        try:
            snapshot_ids = list()
            response = client.describe_images(ImageIds=[ami_id])

            for r in response['Images']:
                for device in r['BlockDeviceMappings']:
                    snapshot_ids.append(device['Ebs']['SnapshotId'])
            return snapshot_ids

        except Exception as e:
            print('Error: Failed to retrieve snapshot IDs for {}'.format(ami_id))
            print(e)
        return []

    @staticmethod
    def create_tags(client, resource_id_list, instance_id, ami_name, backup_tag, billing):
        print('Creating tags for {} ...'.format(resource_id_list))
        try:
            client.create_tags(
                Resources=resource_id_list,
                Tags=[
                    {'Key': 'Name', 'Value': ami_name},
                    {'Key': TAG_KEY_AUTOSNAP_ID, 'Value': instance_id},
                    {'Key': TAG_KEY_AUTOSNAP_LABEL, 'Value': backup_tag},
                    {'Key': TAG_KEY_BILLING, 'Value': billing},
                ]
            )
            print('Created tag {} with value {}'.format(TAG_KEY_AUTOSNAP_ID, instance_id))
            print('Created tag {} with value {}'.format(TAG_KEY_AUTOSNAP_LABEL, backup_tag))
            print('Created tag {} with value {}'.format(TAG_KEY_BILLING, billing))
            return True

        except Exception as e:
            print('Error: Failed to create tags for {}'.format(resource_id_list))
            print(e)
        return False


def lambda_handler(event, context):
    """
    Entry point for triggering from a AWS Lambda job
    """
    helper = AwsTaggingHelper()
    helper.configure_from_lambda_event(event)
    helper.start_process()


if __name__ == '__main__':
    """
    Entry point for running from command line
    """
    # TODO change profile_name
    helper = AwsTaggingHelper(profile_name='default-profile')
    helper.start_process()

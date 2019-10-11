#!/usr/bin/env python
from __future__ import absolute_import
import argparse
import boto3
import datetime


# App defaults
DEFAULTS = {
    'ec2_regions': ['ap-southeast-2'],
    'backup_tag': 'daily',
    'days_to_keep': 7,
}

TAG_KEY_AUTOSNAP_LABEL = 'EC2-Snapper-Label'
DATETIME_STR_FORMAT = '%Y-%m-%dT%H:%M:%S.000z'


class DeleteEC2Backups(object):

    def __init__(self, profile_name=None):
        self._loaded = False
        self.profile_name = profile_name
        self.ec2_regions = list()
        self.backup_tag = DEFAULTS['backup_tag']
        self.days_to_keep = DEFAULTS['days_to_keep']

    def _load_config(self):
        if self._loaded:
            return

        parser = argparse.ArgumentParser(description='Delete expired EC2 backups')
        parser.add_argument('--regions', metavar='region', nargs='*',
                            help='EC2 Region(s) to process for snapshots',
                            default=DEFAULTS['ec2_regions'])
        parser.add_argument('--backup_tag', dest='backup_tag',
                            default=DEFAULTS['backup_tag'], metavar='TAG',
                            help='The tag categorising the backup (defaults to "daily".')
        parser.add_argument('--days_to_keep', dest='days_to_keep', type=int,
                            default=DEFAULTS['days_to_keep'], metavar='[INTEGER]',
                            help='Keep the AMI (and the corresponding snapshots) backup created within days_to_keep')
        settings = parser.parse_args()

        for region in settings.regions:
            self.ec2_regions.append(region)
        self.backup_tag = settings.backup_tag
        self.days_to_keep = int(settings.days_to_keep)

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
            try:
                self.delete_old_backups(region)
            except Exception as e:
                print('Error: Failed to delete backups for region {}'.format(region))
                print(e)

    def delete_old_backups(self, region):
        """
        Remove old backups (AMIs and snapshots)
        """
        self._load_config()

        print('Started removing old AMIs and snapshots with tag [{}] older than {} days ...'\
            .format(self.backup_tag, self.days_to_keep))

        today = datetime.datetime.utcnow()

        client = self.ec2_client(region=region, profile_name=self.profile_name)

        # find all AMIs having tag "EC2-Snapper-Label" = backup_tag
        response = client.describe_images(Filters=[{
            'Name': 'tag:{}'.format(TAG_KEY_AUTOSNAP_LABEL),
            'Values': [self.backup_tag]
        }])

        for image in response['Images']:
            image_date = datetime.datetime.strptime(image['CreationDate'], DATETIME_STR_FORMAT)

            # delete old AMI (and the corresponding snapshots
            if today - image_date > datetime.timedelta(days=self.days_to_keep):
                self.delete_image_and_snapshots(client, image, image_date)

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
    def delete_image_and_snapshots(client, image, image_date):
        ami_id = image['ImageId']

        print('------------------------------------------------------------')
        print('Removing AMI {} created on {} ...'.format(ami_id, image_date))
        client.deregister_image(ImageId=ami_id)

        for device in image['BlockDeviceMappings']:
            snapshot_id = device['Ebs']['SnapshotId']

            print('Removing snapshot {} of {} ...'.format(snapshot_id, ami_id))
            client.delete_snapshot(SnapshotId=snapshot_id)


def lambda_handler(event, context):
    """
    Entry point for triggering from a AWS Lambda job
    """
    helper = DeleteEC2Backups()
    helper.configure_from_lambda_event(event)
    helper.start_process()


if __name__ == '__main__':
    """
    Entry point for running from command line
    """
    # TODO change profile_name
    helper = DeleteEC2Backups(profile_name='default-profile')
    helper.start_process()

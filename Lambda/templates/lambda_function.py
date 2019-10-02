import boto3
import logging

# Update the root logger to get messages at DEBUG and above
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger("botocore").setLevel(logging.CRITICAL)
logging.getLogger("boto3").setLevel(logging.CRITICAL)
logging.getLogger("urllib3.connectionpool").setLevel(logging.CRITICAL)

logging.info(f"boto3.__version__: {boto3.__version__}")

# App defaults
DEFAULTS = {
    "ec2_region": "ap-southeast-2",
}


class Helper(object):
    def __init__(self, profile_name=None):
        self.profile_name = profile_name

    def configure_from_lambda_event(self, event_details):
        for setting in DEFAULTS.keys():
            if setting in event_details:
                self.__setattr__(setting, event_details[setting])
            else:
                self.__setattr__(setting, DEFAULTS[setting])

    def start_process(self):
        pass


def lambda_handler(event, context):
    """Entry point for triggering from a AWS Lambda job
    """
    helper = Helper()
    helper.configure_from_lambda_event(event)
    helper.start_process()


if __name__ == "__main__":
    """Entry point for running from command line
    """
    # TODO change profile_name
    helper = Helper(profile_name="default")
    helper.start_process()

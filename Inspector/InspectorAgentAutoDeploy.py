"""
This is an AWS Lambda job to automatically deploy Inspector agent to newly-launched EC2 instances.

The job requires that the EC2 instance have the SSM (EC2 Simple System Manager) agent installed, and the agent must
have a role attached with necessary SSM permissions. The easiest way to do this is with userdata at instance launch:
https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/install-ssm-agent.html

The job is triggered by a CloudWatch event every time a new instance enters the running state. The job checks to make
sure that the SSM agent is running. It then uses SSM to install and start the Inspector agent.

Modified from https://github.com/awslabs/amazon-inspector-agent-autodeploy/blob/master/autodeploy.py
"""
import boto3
import datetime
import logging

# Update the root logger to get messages at DEBUG and above
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger("botocore").setLevel(logging.CRITICAL)
logging.getLogger("boto3").setLevel(logging.CRITICAL)
logging.getLogger("urllib3.connectionpool").setLevel(logging.CRITICAL)
logging.info(f"boto3.__version__: {boto3.__version__}")


# quick function to handle datetime serialization problems
enco = lambda obj: (
    obj.isoformat()
    if isinstance(obj, datetime.datetime)
       or isinstance(obj, datetime.date)
    else None
)


def lambda_handler(event, context):
    ssm = boto3.client("ssm")
    inspector = boto3.client("inspector")

    logging.debug("Raw Lambda event:")
    logging.debug(event)
    
    # check to ensure that this is an EC2 state change message
    eventType = event["detail-type"]
    if eventType != "EC2 Instance State-change Notification":
        logging.info("Not an EC2 state change notification, exiting: " + eventType)
        return 1
    
    # check to ensure that the new state is "running"
    newState = event["detail"]["state"]
    if newState != "running":
        logging.info("Not an EC2 state change notification, exiting: " + newState)
        return 1
    
    # get the instance ID
    instanceId = event["detail"]["instance-id"]
    logging.info("Instance ID: " + instanceId)
    
    # query SSM for information about this instance
    filterList = [{"key": "InstanceIds", "valueSet": [instanceId]}]
    response = ssm.describe_instance_information(InstanceInformationFilterList=filterList, MaxResults=50)
    logging.debug("SSM DescribeInstanceInformation response:")
    logging.debug(response)
    
    # ensure that the SSM agent is running on the instance
    if len(response) == 0:
        logging.info("SSM agent is not running on the target instance, exiting")
        return 1
    
    # get SSM metadata about the instance
    # assumption: len(InstanceInformationList) == 1 --> not explicitly checking
    instanceInfo = response["InstanceInformationList"][0]
    logging.debug("Instance information:")
    logging.debug(instanceInfo)
    pingStatus = instanceInfo["PingStatus"]
    logging.info("SSM status of instance: " + pingStatus)
    lastPingTime = instanceInfo["LastPingDateTime"]
    logging.debug("SSM last contact:")
    logging.debug(lastPingTime)
    agentVersion = instanceInfo["AgentVersion"]
    logging.debug("SSM agent version: " + agentVersion)
    platformType = instanceInfo["PlatformType"]
    logging.info("OS type: " + platformType)
    osName = instanceInfo["PlatformName"]
    logging.info("OS name: " + osName)
    osVersion = instanceInfo["PlatformVersion"]
    logging.info("OS version: " + osVersion)
    
    # Terminate if SSM agent is offline
    if pingStatus != "Online":
        logging.info("SSM agent for this instance is not online, exiting: " + pingStatus)
        return 1
    
    # This script only supports agent installation on Linux
    if platformType != "Linux":
        logging.info("Skipping non-Linux platform: " + platformType)
        return 1
    
    # set the command to deploy the inspector agent (note that curl and bash are required)
    commandLine = "cd /tmp; curl -O https://d1wk0tztpsntt1.cloudfront.net/linux/latest/install; bash /tmp/install"
    logging.info("Command line to execute: " + commandLine)
    
    # Run the command with SSM
    response = ssm.send_command(
        InstanceIds=[instanceId],
        DocumentName="AWS-RunShellScript",
        Comment="Lambda function performing Inspector agent installation",
        Parameters={"commands": [commandLine]}
    )
    
    logging.info("SSM send-command response:")

    logging.info(response)

"""
This is an AWS Lambda job to automatically patch EC2 instances when an inspector assessment generates a CVE finding.
- The job requires that the EC2 instance to be patched have the SSM (EC2 Simple System Manager) agent installed, and
  the agent must have a role attached with necessary SSM permissions.
- The job is triggered by an SNS notification of a new finding from Inspector. The job checks to make sure that the
  finding is a CVE missing patch finding, and if so, it checks to ensure tha the SSM agent is running. It then uses
  SSM to issue the appropriate patch-and-reboot commands to either Ubuntu or Amazon Linux.

Modified from https://github.com/awslabs/amazon-inspector-auto-remediate/blob/master/lambda-auto-remediate.py
"""
import boto3
import datetime
import json
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
    
    # extract the message that Inspector sent via SNS
    message = event["Records"][0]["Sns"]["Message"]
    logging.debug("Event from SNS: " + message)
    
    # get inspector notification type
    notificationType = json.loads(message)["event"]
    logging.info("Inspector SNS message type: " + notificationType)
    
    # skip everything except report_finding notifications
    if notificationType != "FINDING_REPORTED":
        logging.info("Skipping notification that is not a new finding: " + notificationType)
        return 1
    
    # extract finding ARN
    findingArn = json.loads(message)["finding"]
    logging.info("Finding ARN: " + findingArn)
    
    # get finding and extract detail
    response = inspector.describe_findings(findingArns=[findingArn], locale="EN_US")
    logging.debug("Inspector DescribeFindings response:")
    logging.debug(response)
    finding = response["findings"][0]
    logging.debug("Raw finding:")
    logging.debug(finding)
    
    # skip uninteresting findings
    title = finding["title"]
    logging.debug("Finding title: " + title)
    
    if title == "Unsupported Operating System or Version":
        logging.info("Skipping finding: " + title)
        return 1
    
    if title == "No potential security issues found":
        logging.info("Skipping finding: " + title)
        return 1
    
    service = finding["service"]
    logging.debug("Service: " + service)
    if service != "Inspector":
        logging.info("Skipping finding from service: " + service)
        return 1
    
    cveId = ""
    for attribute in finding["attributes"]:
        if attribute["key"] == "CVE_ID":
            cveId = attribute["value"]
            break
    logging.info("CVE ID: " + cveId)
    
    if cveId == "":
        logging.info("Skipping non-CVE finding (could not find CVE ID)")
        return 1
    
    assetType = finding["assetType"]
    logging.debug("Asset type: " + assetType)
    if assetType != "ec2-instance":
        logging.info("Skipping non-EC2-instance asset type: " + assetType)
        return 1
    
    instanceId = finding["assetAttributes"]["agentId"]
    logging.info("Instance ID: " + instanceId)
    if not instanceId.startswith("i-"):
        logging.info("Invalid instance ID: " + instanceId)
        return 1
    
    # if we got here, we have a valid CVE type finding for an EC2 instance with a well-formed instance ID
    
    # query SSM for information about this instance
    filterList = [{"key": "InstanceIds", "valueSet": [instanceId]}]
    response = ssm.describe_instance_information(InstanceInformationFilterList=filterList, MaxResults=50)
    logging.debug("SSM DescribeInstanceInformation response:")
    logging.debug(response)
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
        logging.info("SSM agent for this instance is not online: " + pingStatus)
        return 1
    
    # This script only supports remediation on Linux
    if platformType != "Linux":
        logging.info("Skipping non-Linux platform: " + platformType)
        return 1
    
    # Look up the correct command to update this Linux distro
    # to-do: patch only CVEs, or patch only the specific CVE
    if osName == "Ubuntu":
        commandLine = "apt-get update -qq -y; apt-get upgrade -y"
    elif osName == "Amazon Linux AMI":
        commandLine = "yum update -q -y; yum upgrade -y"
    else:
        logging.info("Unsupported Linux distribution: " + osName)
        return 1
    logging.info("Command line to execute: " + commandLine)
    
    # now we SSM run-command
    response = ssm.send_command(
        InstanceIds=[instanceId],
        DocumentName="AWS-RunShellScript",
        Comment="Lambda function performing Inspector CVE finding auto-remediation",
        Parameters={"commands": [commandLine]}
    )
    
    logging.info("SSM send-command response:")


    logging.info(response)

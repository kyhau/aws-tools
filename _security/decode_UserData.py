"""
Decode EC2's UserData
"""
import base64
import boto3


instance_id = ""

resp = boto3.client("ec2").describe_instance_attribute(
    Attribute="userData",
    InstanceId=instance_id
)

print(base64.b64decode(resp["UserData"]["Value"]))

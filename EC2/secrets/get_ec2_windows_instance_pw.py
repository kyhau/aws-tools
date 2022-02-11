from base64 import b64decode
from boto3.session import Session
import click
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key


def decrypt(ciphertext, keyfile):
    """
    Decrypt the password using the EC2 pem file.
    See https://cryptography.io/en/latest/hazmat/primitives/asymmetric/serialization/
    """
    with open(keyfile, "rb") as key_file:
        data = key_file.read()
    
    # password = None if the private key is not encrypted
    private_key = load_pem_private_key(data, password=None, backend=default_backend())
    return private_key.decrypt(ciphertext, padding.PKCS1v15())


def get_tag_value(tags, key="Name"):
    for tag in tags:
        if tag["Key"] == key:
            return tag["Value"]
    return ""


@click.command()
@click.option("--instanceid", "-i", help="EC2 instance ID. Check all instances if not specified.")
@click.option("--pemfile", "-f", required=True, help="PEM file.")
@click.option("--profile", "-p", default="default", show_default=True, help="AWS profile name.")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS Region.")
def inspect_ec2_instances(instanceid, pemfile, profile, region):

    session = Session(profile_name=profile)
    client = session.client("ec2", region_name=region)
    kwargs = {"InstanceIds": [instanceid]} if instanceid else {}
    
    for page in client.get_paginator("describe_instances").paginate(**kwargs).result_key_iters():
        for item in page:
            for instance in item["Instances"]:
                instance_id = instance["InstanceId"]
                pw_data = client.get_password_data(InstanceId=instance_id)["PasswordData"]
                if pw_data:
                    data = [
                        instance_id,
                        get_tag_value(instance["Tags"]),
                        instance.get("PrivateIpAddress"),
                        instance.get("PublicIpAddress", "NoPublicIP"),
                        decrypt(b64decode(pw_data), pemfile).decode("ascii"),
                    ]
                    print(",".join(data))
                if kwargs.get("InstanceIds"):
                    return


if __name__ == "__main__":
    inspect_ec2_instances()

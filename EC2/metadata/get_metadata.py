import base64
import os

get_endpoint = lambda endpoint: os.system(f"curl http://169.254.169.254{endpoint}")

public_ip = os.system("curl ifconfig.co")

# Reverse DNS lookup
dns_lookup = lambda ip: os.system(f"nslookup {ip}")

decode_data = lambda x: base64.b64decode(x)

print("[*] AMI ID")
get_endpoint("/latest/meta-data/ami-id")

print("[*] Security credentials")
get_endpoint("/latest/meta-data/iam/security-credentials/")

print("[*] User script")
get_endpoint("/latest/user-data/")

print("[*] Instance role")
role_name = None
get_endpoint(f"/latest/meta-data/iam/security-credentials/{role_name}")

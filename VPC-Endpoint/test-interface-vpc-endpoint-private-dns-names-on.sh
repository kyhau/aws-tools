#!/bin/bash
set -e

# Ref: https://repost.aws/knowledge-center/vpc-fix-gateway-or-interface-endpoint

# With private DNS names turned on, you can run AWS API calls against the service endpoints (for example, ec2.us-east-1.amazonaws.com).
# These resolve to the private IPs of the endpoint interfaces.

# If you don't have private DNS names turned on, then you can run the API calls by explicitly specifying the Regional or zonal VPC endpoint DNS name.

SERVICE_ENDPOINT=codeartifact.ap-southeast-2.amazonaws.com
VPC_ENDPOINT_1=com.amazonaws.ap-southeast-2.codeartifact.api  # private dns name disabled
VPC_ENDPOINT_2=com.amazonaws.ap-southeast-2.codeartifact.repositories  # private dns name enabled


echo "CheckPt: Verify DNS resolution for the interface VPC endpoint name that you're trying to connect to"

# Use the dig or nslookup commands to verify the DNS resolution for the interface VPC endpoint name that you're trying to connect to.
nslookup ${SERVICE_ENDPOINT}


echo "CheckPt: Testing connectivity to interface VPC endpoints"

telnet ${SERVICE_ENDPOINT} 443


VPCE_DNS=$(aws ec2 describe-vpc-endpoints --filters Name=service-name,Values=${VPC_ENDPOINT_2} --query 'VpcEndpoints[*].DnsEntries[0].DnsName' --output text)
echo "VPCE_DNS = $VPCE_DNS"

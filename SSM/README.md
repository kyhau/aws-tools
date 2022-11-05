# SSM


- [AWS Systems Manager Automation runbook reference](https://docs.aws.amazon.com/systems-manager-automation-runbooks/latest/userguide/automation-runbook-reference.html)



### SSM documents and RunCommand

```
# Using aws ssm (simple systems manager)

aws ssm list-documents
aws ssm create-document --content file://ssm-ec2-config.json --name "ssm-ec2-cyberduck-config-v1"
aws ssm create-association --instance-id <instance_id> --name "ssm-ec2-cyberduck-config-v1"
aws ssm delete-document --name "ssm-ec2-cyberduck-config-v1"
```

### SSM Session Manager

For Powershell users, see
https://docs.aws.amazon.com/powershell/latest/reference/items/SimpleSystemsManagement_cmdlets.html

```
################################################################################
# Starting a Session (AWS CLI)
aws ssm start-session --target instance-id

# Starting a Session (Port Forwarding)
aws ssm start-session --target instance-id --document-name AWS-StartPortForwardingSession \
--parameters '{"portNumber":["80"], "localPortNumber":["56789"]}'

# Starting a Session (Interactive Commands)
aws ssm start-session --target instance-id --document-name TestInteractiveCommandSessionDocument \
--parameters '{"logpath":["/var/log/amazon/ssm/amazon-ssm-agent.log"]}'


################################################################################
# Terminating a Session (AWS CLI)
aws ssm terminate-session --session-id session-id


################################################################################
# Starting a Session (SSH)
ssh -i /path/my-key-pair.pem username@instance-id

# Copy local file to the instance
scp -i /path/my-key-pair.pem /path/SampleFile.txt username@instance-id:~

```
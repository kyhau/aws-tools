# SSM

- [AWS Systems Manager Automation runbook reference](https://docs.aws.amazon.com/systems-manager-automation-runbooks/latest/userguide/automation-runbook-reference.html)
- [SessionManager](SessionManager.md)

```
################################################################################
# Using aws ssm (simple systems manager)

aws ssm list-documents
aws ssm create-document --content file://ssm-ec2-config.json --name "ssm-ec2-cyberduck-config-v1"
aws ssm create-association --instance-id <instance_id> --name "ssm-ec2-cyberduck-config-v1"
aws ssm delete-document --name "ssm-ec2-cyberduck-config-v1"


```
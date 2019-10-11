# EC2 / VPC

- [EC2 Instance Connect](EC2InstanceConnect.md)
- [Using Auto Scaling lifecycle hooks, Lambda, and EC2 Run Command](
  https://github.com/aws-samples/aws-lambda-lifecycle-hooks-function)

```
################################################################################
# Resize EBS of a Ubuntu
sudo growpart /dev/xvda 1
sudo resize2fs /dev/xvda1

################################################################################
# Find IP in security group
aws ec2 describe-security-groups --profile my_profile --filters Name=ip-permission.from-port,Values=22 Name=ip-permission.cidr,Values='61.11.11.11/32' Name=ip-permission.cidr,Values='61.22.22.22/32' --query SecurityGroups[*].{groupId:GroupId}

```


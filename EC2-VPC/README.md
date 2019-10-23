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

### List AMIs

```
# List all public AMIs, including any public AMIs that you own.
aws ec2 describe-images --executable-users all

# List AMIs with explicit launch permissions, does not include any AMIs that you own.
aws ec2 describe-images --executable-users self

# List AMIs owned by Amazon
aws ec2 describe-images --owners amazon

# List AMIs owned by an account
aws ec2 describe-images --owners 123456789012

# Scope AMIs using a filter
# To reduce the number of displayed AMIs, use a filter to list only the types of AMIs that interest you. For example, use the following filter to display only EBS-backed AMIs.
# --filters "Name=root-device-type,Values=ebs"
```
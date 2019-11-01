# EC2 Instance Connect

There is no need to install the EC2 Instance Connect CLI if users only use the console or an SSH client to connect
to an instance. 

```
################################################################################
# Install CLI
# https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-connect-set-up.html#ec2-instance-connect-install-eic-CLI

pip install ec2instanceconnectcli

# SSH connection to an instance
mssh <instance_id>

```
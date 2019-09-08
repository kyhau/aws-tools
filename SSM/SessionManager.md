# Session Manager

```
################################################################################
# Viewing Session History (AWS CLI)
aws ssm describe-sessions --state History


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
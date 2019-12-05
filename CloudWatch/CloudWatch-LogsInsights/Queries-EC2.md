### EC2 hosts that were started or stopped in a given Region.
- Log group: cloudtrail (e.g. /aws/cloudtrail)
```
filter (eventName="StartInstances" or eventName="StopInstances") and region="ap-southeast-2"
```

### EC2 terminated by Auto Scaling
- Log group: cloudtrail (e.g. /aws/cloudtrail)
- Filters:
    - eventName == "DeregisterInstancesFromLoadBalancer"
    - eventName == "TerminateInstanceInAutoScalingGroup"
    - eventName == "TerminateInstances"
```
fields @timestamp, @message
| sort @timestamp desc
| filter userAgent == "autoscaling.amazonaws.com" and eventName == "DeregisterInstancesFromLoadBalancer"

fields @timestamp, @message
| sort @timestamp desc
| filter userAgent == "autoscaling.amazonaws.com" and eventName like "TerminateInstance"
```

### Number of log entries by region and EC2 event type.
```
filter eventSource="ec2.amazonaws.com"
| stats count(*) as eventCount by eventName, awsRegion
| sort eventCount desc
```

# EC2 related queries

### EC2 hosts that were started or stopped in a given Region.
- Log group: cloudtrail (e.g. /aws/cloudtrail)
- Filters
    - `eventName = "StartInstances"`
    - `eventName = "StopInstances"`

```
filter (eventName="StartInstances" or eventName="StopInstances") and region="ap-southeast-2"
```

### Auto scaling - start/terminate EC2 instances
- Log group: cloudtrail (e.g. /aws/cloudtrail)
- Filters
    - `eventSource = "autoscaling.amazonaws.com"`
    - `userAgent = "autoscaling.amazonaws.com"`
    - `eventName = "RunInstances"`
    - `eventName = "TerminateInstances"`
    
```
filter (eventName = "RunInstances" or eventName = "TerminateInstances")
```

### EC2 terminated by Auto Scaling
- Log group: cloudtrail (e.g. /aws/cloudtrail)
- Filters:
    - `userAgent = "autoscaling.amazonaws.com"`
    - `eventName == "DeregisterInstancesFromLoadBalancer"`
    - `eventName == "TerminateInstanceInAutoScalingGroup"`
    - `eventName == "TerminateInstances"`
    - `eventName like "TerminateInstance"`

```
fields @timestamp, @message
| sort @timestamp desc
| filter userAgent == "autoscaling.amazonaws.com" and eventName == "DeregisterInstancesFromLoadBalancer"

fields @timestamp, @message
| sort @timestamp desc
| filter userAgent == "autoscaling.amazonaws.com" and eventName like "TerminateInstance"
```

### Number of log entries by region and EC2 event type.
- Log group: cloudtrail (e.g. /aws/cloudtrail)

```
filter eventSource="ec2.amazonaws.com"
| stats count(*) as eventCount by eventName, awsRegion
| sort eventCount desc
```

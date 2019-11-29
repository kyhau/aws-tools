EC2 hosts that were started or stopped in a given Region.
- Log group: cloudtrail (e.g. /aws/cloudtrail)
```
filter (eventName="StartInstances" or eventName="StopInstances") and region="ap-southeast-2"
```

Number of log entries by region and EC2 event type.
```
filter eventSource="ec2.amazonaws.com"
| stats count(*) as eventCount by eventName, awsRegion
| sort eventCount desc
```

User has problem accessing EC2 Console
- (Use Policy Simulator first)
- Log group: cloudtrail (e.g. /aws/cloudtrail)
- Filters
    - `errorCode = "Client.UnauthorizedOperation"` 
    - `userAgent = "console.ec2.amazonaws.com"`
    - `eventName = "DescribeInstances"`, or `eventName like "Describe"` 
- Check `awsRegion`, may be just ended up in wrong region.
```
fields @timestamp, @message
| filter userAgent = "console.ec2.amazonaws.com" and eventName like "Describe" and @message like /todo.username/  
| sort @timestamp desc
| limit 5
```

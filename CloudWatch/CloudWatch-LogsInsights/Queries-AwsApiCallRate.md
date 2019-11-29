AwsApiCall Rate exceeded
- Log group: cloudtrail (e.g. /aws/cloudtrail)
```
fields @timestamp, eventSource, eventName, sourceIPAddress, userIdentity.arn, @message
| sort @timestamp desc
| limit 200
| filter (eventType = "AwsApiCall" and @message like /(?i)(Rate exceeded)/)
```

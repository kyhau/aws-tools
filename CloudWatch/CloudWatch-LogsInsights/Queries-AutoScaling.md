Auto scaling
- Log group: cloudtrail (e.g. /aws/cloudtrail)
- Filters
    - `eventSource = "autoscaling.amazonaws.com"`
    - `userAgent = "autoscaling.amazonaws.com"`
    - `eventName = "RunInstances"`
    - `eventName = "TerminateInstances"`
    
```
filter (eventName="RunInstances" or eventName="TerminateInstances")"
```

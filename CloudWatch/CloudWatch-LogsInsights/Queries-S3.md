Find S3 presigned url usage

```
fields @timestamp, @message
| filter eventSource = "s3.amazonaws.com" and (eventName = "GetObject" or eventName = "PutObject") and ispresent(requestParameters.Expires)
| sort @timestamp desc
| limit 20
```

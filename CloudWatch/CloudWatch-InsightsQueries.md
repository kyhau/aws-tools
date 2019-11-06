# Some useful CloudWatch Logs Insights queries

- [Common](#common)
- [CloudTrail Logs](#cloudtrail-logs)
- [Lambda Logs](#lambda-logs)
- [VPC Flow Logs](#vpc-flow-logs)
- [Route 53 Logs](#route-53-logs)
- [AppSync Logs](#appsync-logs)
- [API Rate Limits](#awsapicall-rate)

See also 
- https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax.html#CWL_QuerySyntax-operations-functions
- https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax-examples.html. 

---

### Common

25 most recently added log events.
```
fields @timestamp, @message | sort @timestamp desc | limit 25
```

List of log events that are not exceptions.
```
fields @message | filter @message not like /Exception/
```

Number of exceptions logged per hour.
```
filter @message like /Exception/ 
| stats count(*) as exceptionCount by bin(1h)
| sort exceptionCount desc
```

Use a glob expression to extract the ephemeral fields @user, @method, and @latency from the log field @message and
return the average latency for each unique combination of @method and @user.
```
parse @message "user=*, method:*, latency := *" as @user, @method, @latency 
| stats avg(@latency) by @method, @user
```

Use a regular expression to extract the ephemeral fields @user2, @method2, and @latency2 from the log field @message a
nd return the average latency for each unique combination of @method2 and @user2.
```
parse @message /user=(?<user2>.*?), method:(?<method2>.*?), latency := (?<latency2>.*?)/ 
| stats avg(@latency2) by @method2, @user2
```

### CloudTrail Logs

Number of log entries for each service, event type, and Region.
```
stats count(*) by eventSource, eventName, awsRegion
```

Number of log entries by region and EC2 event type.
```
filter eventSource="ec2.amazonaws.com"
| stats count(*) as eventCount by eventName, awsRegion
| sort eventCount desc
```

EC2 hosts that were started or stopped in a given Region.
```
filter (eventName="StartInstances" or eventName="StopInstances") and region="us-east-2"
```

Number of records where an exception occurred while invoking the API UpdateTrail.
```
filter eventName="UpdateTrail" and ispresent(errorCode)
| stats count(*) by errorCode, errorMessage
```

Regions, usernames, and ARNs of newly created IAM users.
```
filter eventName="CreateUser"
| fields awsRegion, requestParameters.userName, responseElements.user.arn
```

### Lambda Logs

Determine the amount of overprovisioned memory.
```
filter @type = "REPORT"
| stats max(@memorySize / 1024 / 1024) as provisonedMemoryMB,
    min(@maxMemoryUsed / 1024 / 1024) as smallestMemoryRequestMB,
    avg(@maxMemoryUsed / 1024 / 1024) as avgMemoryUsedMB,
    max(@maxMemoryUsed / 1024 / 1024) as maxMemoryUsedMB,
    provisonedMemoryMB - maxMemoryUsedMB as overProvisionedMB
```

Report latency statistics for 5-minute intervals.
```
filter @type = "REPORT" 
| stats avg(@duration), max(@duration), min(@duration) by bin(5m)
```

Find the most expensive requests
```
filter @type = "REPORT"
| fields @requestId, @billedDuration
| sort by @billedDuration desc
```

### VPC Flow Logs

IP addresses using UDP as a data transfer protocol.
```
filter protocol=17 | stats count(*) by srcAddr
```

IP addresses (top 20) with highest number of rejected requests.
```
filter action="REJECT"
| stats count(*) as numRejections by srcAddr
| sort numRejections desc | limit 20
```

Avg, min and max byte transfers by source and destination IP addresses.
```
stats avg(bytes), min(bytes), max(bytes) by srcAddr, dstAddr
```

Top 15 byte transfers by source and destination IP addresses.
```
stats sum(bytes) as bytesTransferred by srcAddr, dstAddr
| sort bytesTransferred desc | limit 15
```

Top 15 byte transfers for a given host.
```
filter srcAddr LIKE "192.0.2."
| stats sum(bytes) as bytesTransferred by dstAddr
| sort bytesTransferred desc | limit 15
```

Top 15 packet transfers across hosts.
```
stats sum(packets) as packetsTransferred by srcAddr, dstAddr
| sort packetsTransferred  desc | limit 15
```

IP addresses where flow records were skipped during the capture window.
```
filter logStatus="SKIPDATA"
| stats count(*) by bin(1h) as t
| sort t
```

### Route 53 Logs

Number of requests received every 10 minutes by edge location.
```
stats count(*) by queryType, bin(10m)
```

Number of unsuccessful requests by domain and subdomain.
```
filter responseCode="SERVFAIL" | stats count(*) by queryName
```

DNS resolvers (top 10) with highest number of requests.
```
stats count(*) as numRequests by resolverIp
| sort numRequests desc | limit 10
```

### AppSync Logs

Number of unique HTTP status codes
```
fields ispresent(graphQLAPIId) as isApi
| filter isApi | filter logType = "RequestSummary"
| stats count() as statusCount by statusCode
| sort statusCount desc
```

Resolvers (top 10) with maximum latency
```
fields resolverArn, duration
| filter logType = "Tracing"
| sort duration desc | limit 10
```

Most frequently invoked resolvers
```
fields ispresent(resolverArn) as isRes
| stats count() as invocationCount by resolverArn
| filter isRes | filter logType = "Tracing"
| sort invocationCount desc | limit 10
```

Resolvers with most errors in mapping templates
```
fields ispresent(resolverArn) as isRes
| stats count() as errorCount by resolverArn, logType
| filter isRes and (logType = "RequestMapping" or logType = "ResponseMapping") and fieldInError
| sort errorCount desc | limit 10
```

Field latency statistics
```
stats min(duration), max(duration), avg(duration) as avgDur by concat(parentType, '/', fieldName) as fieldKey
| filter logType = "Tracing"
| sort avgDur desc | limit 10
```

Resolver latency statistics
```
fields ispresent(resolverArn) as isRes
| filter isRes | filter logType = "Tracing"
| stats min(duration), max(duration), avg(duration) as avgDur by resolverArn
| sort avgDur desc | limit 10 
```

Requests (top 10) with maximum latency
```
fields requestId, latency
| filter logType = "RequestSummary"
| sort latency desc | limit 10
```


### AwsApiCall Rate

AwsApiCall Rate exceeded
```
fields @timestamp, eventSource, eventName, sourceIPAddress, userIdentity.arn, @message
| sort @timestamp desc
| limit 200
| filter (eventType = "AwsApiCall" and @message like /(?i)(Rate exceeded)/)
```

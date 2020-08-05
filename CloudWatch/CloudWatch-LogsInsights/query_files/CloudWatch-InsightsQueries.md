# Some useful CloudWatch Logs Insights queries

- [Common](#common)
- [CloudTrail Logs](#cloudtrail-logs)
- [Route 53 Logs](#route-53-logs)
- [AppSync Logs](#appsync-logs)

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

# Some useful CloudTrail `lookup-events` queries

### Notes
See also https://docs.aws.amazon.com/en_pv/awscloudtrail/latest/userguide/view-cloudtrail-events-cli.html.

1. AttributeKey` values:
   - `AccessKeyId` (e.g. `AKIAIOSFODNN7EXAMPLE`)
   - `EventId` (e.g. `b5cc8c40-12ba-4d08-a8d9-2bceb9a3e002`)
   - `EventName` (e.g. `RunInstances`)
   - `EventSource` (e.g. `iam.amazonaws.com`)
   - `ReadOnly` (e.g. `false`)
    - `ResourceName` (e.g. `CloudTrail_CloudWatchLogs_Role`)
   - `ResourceType` (e.g. `AWS::S3::Bucket`)
   - `Username` (e.g. `root`)

2. [Valid `<timestamp>` formats](
    https://docs.aws.amazon.com/awscloudtrail/latest/userguide/view-cloudtrail-events-cli.html#look-up-events-by-time-range-formats)

3. CloudTrail supports logging S3 object-level API operations such as `GetObject`, `DeleteObject`, and `PutObject`.
   These events are called data events. 
   **However, CloudTrail trails do not log data events by default**; you need to enable S3 Object-Level Logging to
   log data events to CloudTrail ([see REF](
   https://docs.aws.amazon.com/AmazonS3/latest/user-guide/enable-cloudtrail-events.html)).


### Common Queries

List all event names for a given resource.
```
RESOURCE_ID=vol-0f59a355c2example     # EBS volume ID
RESOURCE_ID=snap-0993c0d9a8example    # EBS snapshot ID

aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=ResourceName,AttributeValue=${RESOURCE_ID} \
  --query 'Events[].{username:Username,time:EventTime,event:EventName,eventid:EventId,accesskey:AccessKeyId,resource:(Resources[0].ResourceName)}' \
  --output table --region ap-southeast-2
```

List events for a specific API action for a given resource.
```
RESOURCE_ID=vol-0f59a355c2example     # EBS volume ID
API_ACTION=DeleteVolume

aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=ResourceName,AttributeValue=${RESOURCE_ID} \
  --query 'Events[].{username:Username,time:EventTime,event:EventName,eventid:EventId,accesskey:AccessKeyId,resource:(Resources[0].ResourceName)}' \
  --output json --region ap-southeast-2 \
  | jq -r '.[] | select(.event == "${API_ACTION}")'
```

List a specific event name for all resources.
```
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventName,AttributeValue=DeleteVolume \
  --query 'Events[].{username:Username,time:EventTime,event:EventName,eventid:EventId,accesskey:AccessKeyId,resource:(Resources[0].ResourceName)}' \
  --output table --region ap-southeast-2
```

View details for a specific event id.
```
EVENT_ID="0840b15f-75b5-4082-a194-86e15example"
aws cloudtrail lookup-events \
  --lookup-attribute AttributeKey=EventId,AttributeValue=${EVENT_ID} \
  --query "Events[0].CloudTrailEvent" \
  --output text --region ap-southeast-2 \
  | jq -r '.'
```

Specify a date range
```
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventName,AttributeValue=DeleteVolume \
  --query 'Events[].{username:Username,time:EventTime,event:EventName,eventid:EventId,accesskey:AccessKeyId,resource:(Resources[0].ResourceName)}' \
  --start-time 2019-01-01T13:00Z \
  --end-time 2019-03-01T14:00Z \
  --output table --region ap-southeast-2
```


ALTER TABLE cloudtrail_logs_todo ADD
   PARTITION (region='ap-southeast-2',
              year='2020',
              month='06',
              day='12')
   LOCATION 's3://CloudTrail_bucket_name/AWSLogs/Account_ID/CloudTrail/ap-southeast-2/2020/06/12/'